"""E4 AUDIT: weight-only induction-head detection in a tiny transformer.

Recreates the logic of Sparks Experiment 3 (identify copying/induction
heads from weights alone, no forward passes through the audited heads'
behaviour) at small scale:

1. Train a 2-layer transformer on sequences with planted repeats.
2. WEIGHTS-ONLY analysis (Elhage et al. QK/OV circuit composition):
   - find the layer-1 previous-token head from the positional structure
     of its QK matrix;
   - score every layer-2 head by composing its QK circuit through that
     head's OV circuit and measuring token-identity alignment.
3. MEASURED ground truth (forward passes allowed here): each layer-2
   head's attention to the token following a previous occurrence of the
   current token, on planted-repeat sequences.
4. Causal check: ablate the weight-only top head and the other heads;
   compare loss increase on repeat-prediction positions.

Run: .venv-torch/bin/python exp/wsp_e4_audit.py
"""
import json, math, time
from pathlib import Path
import numpy as np
import torch
import torch.nn as nn
import torch.nn.functional as F

torch.manual_seed(20261103); np.random.seed(20261103)
ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "exp" / "results"; OUT.mkdir(parents=True, exist_ok=True)

VOCAB, T, D, H, LAYERS, DM = 24, 32, 64, 4, 2, 128

def make_batch(rng, bs):
    """Sequences of random tokens with one planted repeated bigram:
    ... a b ... a -> (predict b). Returns x, y, repeat_pos mask where
    the target is the repeated bigram's second token."""
    x = rng.integers(0, VOCAB, size=(bs, T))
    rep = np.zeros((bs, T), dtype=bool)
    for i in range(bs):
        a, b = rng.integers(0, VOCAB, size=2)
        p1 = rng.integers(2, T // 2)
        p2 = rng.integers(p1 + 4, T - 1)
        x[i, p1] = a; x[i, p1 + 1] = b
        x[i, p2] = a                      # second occurrence of a
        if p2 + 1 < T:
            x[i, p2 + 1] = b; rep[i, p2] = True   # position p2 predicts b
    y = np.roll(x, -1, axis=1); y[:, -1] = 0
    rep[:, -1] = False
    return (torch.tensor(x), torch.tensor(y), torch.tensor(rep))

class Block(nn.Module):
    def __init__(self):
        super().__init__()
        self.ln1 = nn.LayerNorm(D); self.attn = nn.MultiheadAttention(D, H, batch_first=True)
        self.ln2 = nn.LayerNorm(D)
        self.mlp = nn.Sequential(nn.Linear(D, DM), nn.GELU(), nn.Linear(DM, D))
    def forward(self, x, mask, need_w=False):
        h1 = self.ln1(x)
        a, w = self.attn(h1, h1, h1, attn_mask=mask,
                         need_weights=need_w, average_attn_weights=False)
        x = x + a
        return x + self.mlp(self.ln2(x)), w

class TinyLM(nn.Module):
    def __init__(self):
        super().__init__()
        self.emb = nn.Embedding(VOCAB, D); self.pos = nn.Embedding(T, D)
        self.blocks = nn.ModuleList([Block() for _ in range(LAYERS)])
        self.lnf = nn.LayerNorm(D); self.head = nn.Linear(D, VOCAB, bias=False)
        self.head.weight = self.emb.weight  # tied
    def forward(self, x, ablate=None):
        B, S = x.shape
        mask = torch.triu(torch.full((S, S), float("-inf")), 1)
        h = self.emb(x) + self.pos(torch.arange(S))[None]
        weights = []
        for li, blk in enumerate(self.blocks):
            h, w = blk(h, mask, need_w=(ablate is None and getattr(self, '_want_w', False)))
            if ablate is not None and ablate[0] == li:
                pass
            weights.append(w)
        return self.head(self.lnf(h)), weights

def train(model, steps=6000):
    opt = torch.optim.AdamW(model.parameters(), lr=3e-3, weight_decay=0.01)
    rng = np.random.default_rng(3)
    for s in range(steps):
        x, y, rep = make_batch(rng, 128)
        logits, _ = model(x)
        loss = F.cross_entropy(logits[:, :-1].reshape(-1, VOCAB), y[:, :-1].reshape(-1))
        if s % 1000 == 0:
            with torch.no_grad():
                lp = F.log_softmax(logits[:, :-1], -1)
                nll = -lp.gather(-1, y[:, :-1, None]).squeeze(-1)
                print(f"  repeat loss {nll[rep[:, :-1]].mean().item():.3f}", flush=True)
        opt.zero_grad(); loss.backward(); opt.step()
        if s % 1000 == 0: print(f"step {s} loss {loss.item():.3f}", flush=True)
    return model

@torch.no_grad()
def measured_induction(model, n_batches=12):
    model._want_w = True
    """Mean attention from the repeat position to (first occurrence + 1),
    per layer-2 head, plus final loss on repeat vs other positions."""
    rng = np.random.default_rng(77)
    scores = np.zeros(H); counts = 0
    rep_losses, base_losses = [], []
    for _ in range(n_batches):
        x, y, rep = make_batch(rng, 64)
        logits, weights = model(x)
        w2 = weights[1].numpy()  # (B, H, T, T)
        lp = F.log_softmax(logits[:, :-1], -1)
        nll = -lp.gather(-1, y[:, :-1, None]).squeeze(-1).numpy()
        rep_losses.append(nll[rep[:, :-1]]); base_losses.append(nll[~rep[:, :-1]])
        xn = x.numpy(); rn = rep.numpy()
        for i in range(x.shape[0]):
            ts = np.where(rn[i, :-1])[0]
            for t in ts:
                prev = np.where(xn[i, :t] == xn[i, t])[0]
                if len(prev):
                    scores += w2[i, :, t, prev[0] + 1]; counts += 1
    return scores / max(counts, 1), float(np.concatenate(rep_losses).mean()), float(np.concatenate(base_losses).mean())

def weights_only_analysis(model):
    sd = model.state_dict()
    E = sd["emb.weight"].numpy()                       # (V, D)
    P = sd["pos.weight"].numpy()                       # (T, D)
    def qkv(li, h):
        W = sd[f"blocks.{li}.attn.in_proj_weight"].numpy()   # (3D, D)
        d = D // H
        q = W[0*D + h*d: 0*D + (h+1)*d]; k = W[1*D + h*d: 1*D + (h+1)*d]; v = W[2*D + h*d: 2*D + (h+1)*d]
        Wo = sd[f"blocks.{li}.attn.out_proj.weight"].numpy()  # (D, D)
        return q, k, v, Wo[:, h*d:(h+1)*d]
    # layer-1 previous-token head: positional QK superdiagonal score
    prev_scores = []
    for h in range(H):
        q, k, _, _ = qkv(0, h)
        Apos = (P @ q.T) @ (P @ k.T).T / math.sqrt(D // H)   # (T, T) query x key
        sup = np.mean([Apos[t, t-1] for t in range(1, T)])
        off = (Apos.sum() - np.trace(Apos) - sum(Apos[t, t-1] for t in range(1, T))) / (T*T - T - (T-1))
        prev_scores.append(float(sup - off))
    prev_head = int(np.argmax(prev_scores))
    # OV circuit of that head, in residual space
    _, _, v_w, Wo = qkv(0, prev_head)
    OV = Wo @ v_w                                            # (D, D)
    # layer-2 induction scores: compose QK through OV, token-identity alignment
    ind_scores = []
    for h in range(H):
        q, k, _, _ = qkv(1, h)
        # query side sees residual stream containing OV(prev token info):
        M = (OV.T @ q.T) @ k                                 # (D, D) composed circuit
        A = E @ M @ E.T                                      # (V, V)
        ident = float(np.trace(A) / VOCAB)
        scale = float(np.abs(A).mean() + 1e-12)
        ind_scores.append(ident / scale)
    return prev_scores, prev_head, ind_scores

@torch.no_grad()
def ablation_delta(model, layer=1, n_batches=4):
    """Loss increase on repeat positions when each layer-2 head's output
    is zeroed (via output-projection columns)."""
    rng = np.random.default_rng(55)
    batches = [make_batch(rng, 64) for _ in range(n_batches)]
    def rep_loss(mod):
        tot, n = 0.0, 0
        for x, y, rep in batches:
            logits, _ = mod(x)
            lp = F.log_softmax(logits[:, :-1], -1)
            nll = -lp.gather(-1, y[:, :-1, None]).squeeze(-1)
            tot += nll[rep[:, :-1]].sum().item(); n += int(rep[:, :-1].sum())
        return tot / n
    base = rep_loss(model)
    deltas = {}
    import copy
    for h in range(H):
        m2 = copy.deepcopy(model)
        d = D // H
        with torch.no_grad():
            m2.blocks[layer].attn.out_proj.weight[:, h*d:(h+1)*d] = 0
        deltas[f"head_{h}"] = rep_loss(m2) - base
    return base, deltas

def main():
    t0 = time.time()
    model = train(TinyLM())
    prev_scores, prev_head, ind_scores = weights_only_analysis(model)
    meas_scores, rep_loss, base_loss = measured_induction(model)
    model._want_w = False
    base_rep, deltas = ablation_delta(model)
    wo_rank = list(np.argsort(ind_scores)[::-1]); meas_rank = list(np.argsort(meas_scores)[::-1])
    # spearman by hand (no scipy dependency)
    def rankdata(a):
        order = np.argsort(a); r = np.empty(len(a)); r[order] = np.arange(len(a)); return r
    ra, rb = rankdata(ind_scores), rankdata(meas_scores)
    spear = float(np.corrcoef(ra, rb)[0, 1])
    res = {"model_params": int(sum(p.numel() for p in model.parameters())),
           "layer1_prev_token_scores_weights_only": [round(s, 3) for s in prev_scores],
           "layer1_prev_token_head_weights_only": prev_head,
           "layer2_induction_scores_weights_only": [round(s, 3) for s in ind_scores],
           "layer2_top_head_weights_only": int(wo_rank[0]),
           "layer2_induction_attention_measured": [round(float(s), 4) for s in meas_scores],
           "layer2_top_head_measured": int(meas_rank[0]),
           "top_head_match": bool(wo_rank[0] == meas_rank[0]),
           "spearman_weights_only_vs_measured": spear,
           "repeat_position_loss": rep_loss, "other_position_loss": base_loss,
           "ablation_repeat_loss_base": base_rep,
           "ablation_repeat_loss_delta_by_head": {k: round(v, 4) for k, v in deltas.items()},
           "wall_seconds": round(time.time() - t0, 1)}
    torch.save(model.state_dict(), OUT / "tiny_transformer.pt")
    (OUT / "summary_e4.json").write_text(json.dumps(res, indent=1))
    print(json.dumps(res, indent=1))

if __name__ == "__main__":
    main()
