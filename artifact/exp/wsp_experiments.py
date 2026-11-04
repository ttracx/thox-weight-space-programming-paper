"""Weight-Space Programming recreation experiments E1-E3 (pure NumPy), v2.

E1 READ : train identical MLPs on 3 spatial tasks; read task identity from
          W1 alone with a per-unit axis-voting reader (v2; the v1 global
          marginal reader scored at chance, see FINDINGS_V1.md).
E2 WRITE: hand-write (reasoning, zero gradient steps) the weights of a
          landing-prediction network; compare with random and with a
          gradient-trained baseline granted oracle training targets, in a
          standard and a hard regime.
E3 FIX  : imitation-train a policy into the MountainCar local minimum
          (0% success), then repair it with a sparse surgical weight edit
          (dedicated velocity detectors + energy-pumping override, v2).

Every headline number is written to exp/results/summary_e123.json.
Run: python3 exp/wsp_experiments.py
"""
import json, math, time
from pathlib import Path
import numpy as np

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "exp" / "results"
OUT.mkdir(parents=True, exist_ok=True)
CACHE = OUT / "e1_weights.npz"

# ---------------------------------------------------------------- E1: READ
def make_grid_data(rng, n, task):
    pos = rng.integers(0, 64, size=n)
    x = pos % 8; y = pos // 8
    X = np.zeros((n, 64), dtype=np.float64)
    X[np.arange(n), pos] = 1.0
    X += rng.normal(0, 0.05, X.shape)
    if task == "col":   lab = x // 2
    elif task == "row": lab = y // 2
    elif task == "diag": lab = np.minimum((x + y) * 4 // 15, 3)
    else: raise ValueError(task)
    Y = np.zeros((n, 4)); Y[np.arange(n), lab] = 1.0
    return X, Y

def train_mlp(rng, X, Y, hidden=48, epochs=200, lr=0.01):
    d = X.shape[1]
    W1 = rng.normal(0, math.sqrt(2/d), (d, hidden)); b1 = np.zeros(hidden)
    W2 = rng.normal(0, math.sqrt(2/hidden), (hidden, 4)); b2 = np.zeros(4)
    params = [W1, b1, W2, b2]
    m = [np.zeros_like(p) for p in params]; v = [np.zeros_like(p) for p in params]
    for t in range(1, epochs+1):
        H = np.maximum(X @ W1 + b1, 0)
        Z = H @ W2 + b2; Z -= Z.max(1, keepdims=True)
        P = np.exp(Z); P /= P.sum(1, keepdims=True)
        dZ = (P - Y) / len(X)
        gW2 = H.T @ dZ; gb2 = dZ.sum(0)
        dH = (dZ @ W2.T) * (H > 0)
        grads = [X.T @ dH, dH.sum(0), gW2, gb2]
        for i in range(4):
            m[i] = 0.9*m[i] + 0.1*grads[i]; v[i] = 0.999*v[i] + 0.001*grads[i]**2
            params[i] -= lr * (m[i]/(1-0.9**t)) / (np.sqrt(v[i]/(1-0.999**t)) + 1e-8)
        W1, b1, W2, b2 = params
    H = np.maximum(X @ W1 + b1, 0)
    acc = float((np.argmax(H @ W2 + b2, 1) == np.argmax(Y, 1)).mean())
    return (W1, W2), acc

def conc(profile):
    return float(profile.std() / (profile.mean() + 1e-12))

def unit_axis_scores(A):
    """A: one hidden unit's 8x8 |W1| map. Returns (col,row,diag) scores."""
    col = conc(A.sum(axis=0)); row = conc(A.sum(axis=1))
    diag = conc(np.array([A.diagonal(k).sum() for k in range(-7, 8)]))
    anti = conc(np.array([np.fliplr(A).diagonal(k).sum() for k in range(-7, 8)]))
    return col, row, max(diag, anti)

def read_global_marginal(W1):
    M = np.abs(W1).sum(axis=1).reshape(8, 8)
    scores = {"col": conc(M.sum(axis=0)), "row": conc(M.sum(axis=1)),
              "diag": max(conc(np.array([M.diagonal(k).sum() for k in range(-7, 8)])),
                          conc(np.array([np.fliplr(M).diagonal(k).sum() for k in range(-7, 8)])))}
    return max(scores, key=scores.get), scores

def read_effective(W1, W2, per_class=False):
    """Weight algebra only: effective input->logit map E = W2^T-applied
    to W1 (the linear composition, ignoring ReLU gating)."""
    E = (W2.T @ W1.T)  # (4 classes, 64 inputs)
    if not per_class:
        M = np.abs(E).sum(axis=0).reshape(8, 8)
        scores = {"col": conc(M.sum(axis=0)), "row": conc(M.sum(axis=1)),
                  "diag": max(conc(np.array([M.diagonal(k).sum() for k in range(-7, 8)])),
                              conc(np.array([np.fliplr(M).diagonal(k).sum() for k in range(-7, 8)])))}
        return max(scores, key=scores.get), scores
    votes = {"col": 0.0, "row": 0.0, "diag": 0.0}
    for c in range(E.shape[0]):
        A = np.abs(E[c]).reshape(8, 8)
        sc = {"col": conc(A.sum(axis=0)), "row": conc(A.sum(axis=1)),
              "diag": max(conc(np.array([A.diagonal(k).sum() for k in range(-7, 8)])),
                          conc(np.array([np.fliplr(A).diagonal(k).sum() for k in range(-7, 8)])))}
        win = max(sc, key=sc.get)
        votes[win] += sc[win] - sorted(sc.values())[1]
    return max(votes, key=votes.get), votes

def read_task_from_W1(W1):
    """Per-unit axis voting: each hidden unit votes for the spatial axis
    its receptive field is most selectively organised along; votes are
    weighted by unit magnitude and winning margin. Weights only."""
    votes = {"col": 0.0, "row": 0.0, "diag": 0.0}
    for j in range(W1.shape[1]):
        A = np.abs(W1[:, j]).reshape(8, 8)
        mag = float(A.sum())
        if mag < 1e-9: continue
        c, r, d = unit_axis_scores(A)
        scores = {"col": c, "row": r, "diag": d}
        win = max(scores, key=scores.get)
        margin = scores[win] - sorted(scores.values())[1]
        votes[win] += mag * max(margin, 0.0)
    return max(votes, key=votes.get), votes

def run_e1():
    tasks = ["col", "row", "diag"]
    z = np.load(CACHE) if CACHE.exists() else None
    if z is not None and "W2_0" in z:
        W1s = [z[f"W1_{i}"] for i in range(30)]; W2s = [z[f"W2_{i}"] for i in range(30)]
        labels = list(z["labels"]); accs = list(z["accs"])
    else:
        W1s, W2s, labels, accs = [], [], [], []
        for task in tasks:
            for seed in range(10):
                rng = np.random.default_rng(1000 + 97*seed + (abs(hash(task)) % 1000))
                X, Y = make_grid_data(rng, 1024, task)
                (W1, W2), acc = train_mlp(rng, X, Y)
                W1s.append(W1); W2s.append(W2); labels.append(task); accs.append(acc)
        np.savez(CACHE, **{f"W1_{i}": W1s[i] for i in range(30)},
                 **{f"W2_{i}": W2s[i] for i in range(30)},
                 labels=np.array(labels), accs=np.array(accs))
    readers = {
        "R1_global_marginal_W1": lambda W1, W2, rng: read_global_marginal(W1)[0],
        "R2_per_unit_voting_W1": lambda W1, W2, rng: read_task_from_W1(W1)[0],
        "R3_effective_map": lambda W1, W2, rng: read_effective(W1, W2)[0],
        "R4_effective_per_class": lambda W1, W2, rng: read_effective(W1, W2, per_class=True)[0],
    }
    out = {}
    rng = np.random.default_rng(5)
    for name, fn in readers.items():
        hits = perm = 0; confusion = {}
        for W1, W2, task in zip(W1s, W2s, labels):
            pred = fn(W1, W2, rng); hits += int(pred == task)
            confusion[(task, pred)] = confusion.get((task, pred), 0) + 1
            W1p = rng.permutation(W1.ravel()).reshape(W1.shape)
            perm += int(fn(W1p, W2, rng) == task)
        out[name] = {"accuracy": hits / 30, "permutation_control_accuracy": perm / 30,
                     "confusion": {f"{a}->{b}": n for (a, b), n in sorted(confusion.items()) if a != b}}
    per_task = {t: float(np.mean([a for a, l in zip(accs, labels) if l == t])) for t in tasks}
    best = max(out, key=lambda k: out[k]["accuracy"])
    return {"trained_task_accuracy_mean": per_task, "n_networks": 30, "chance": 1/3,
            "readers": out, "best_reader": best,
            "reader_accuracy": out[best]["accuracy"],
            "permutation_control_accuracy": out[best]["permutation_control_accuracy"]}

# --------------------------------------------------------------- E2: WRITE
def reflect01(x):
    m = np.mod(x, 2.0)
    return np.where(m <= 1.0, m, 2.0 - m)

def written_network():
    """Hand-written weights. NO training. Hidden units compute
    ReLU(s-k), s = bx + 4*vx, k in [-2..3]; output layer applies the
    triangle-wave slope-change coefficients. Verified exact on the
    reachable range s in [-0.9, 1.9] (bx in [0.05,0.95], |vx| <= 0.22)."""
    ks = np.array([-2., -1., 0., 1., 2., 3.])
    coef = np.array([1., -2., 2., -2., 2., -2.])
    W1 = np.zeros((3, 6)); b1 = -ks.copy()
    W1[0, :] = 1.0; W1[1, :] = 4.0
    W2 = coef.reshape(6, 1).copy(); b2 = np.array([0.0])
    s = np.linspace(-0.9, 1.9, 5601)
    err = float(np.max(np.abs(np.maximum(s[:, None] - ks[None, :], 0) @ coef - reflect01(s))))
    return (W1, b1, W2, b2), err

def net_target(net, bx, vx):
    W1, b1, W2, b2 = net
    X = np.stack([bx, vx, np.zeros_like(bx)], axis=1)
    return (np.maximum(X @ W1 + b1, 0) @ W2 + b2).ravel()

def simulate_catch(target_fn, seed, episodes=2000, speed=0.35, window=0.08):
    rng = np.random.default_rng(seed); catches, maes = 0, []
    for _ in range(episodes):
        bx = rng.uniform(0.05, 0.95); vx = rng.uniform(-0.22, 0.22)
        px = rng.uniform(0.1, 0.9)
        landing = float(reflect01(np.array([bx + 4*vx]))[0])
        tgt = float(target_fn(bx, vx)); maes.append(abs(tgt - landing))
        for _ in range(4): px += np.clip(tgt - px, -speed, speed)
        catches += int(abs(px - landing) <= window)
    return catches / episodes, float(np.mean(maes))

def run_e2():
    net, tri_err = written_network()
    fn_w = lambda bx, vx: float(net_target(net, np.array([bx]), np.array([vx]))[0])
    w_catch, w_mae = simulate_catch(fn_w, 7)
    w_catch_h, w_mae_h = simulate_catch(fn_w, 7, speed=0.16, window=0.04)
    r_catches = []
    for sd in range(20):
        r = np.random.default_rng(500 + sd)
        rnet = (r.normal(0, 1, (3, 6)), r.normal(0, 1, 6), r.normal(0, 1, (6, 1)), r.normal(0, 1, 1))
        c, _ = simulate_catch(lambda bx, vx, rn=rnet: float(net_target(rn, np.array([bx]), np.array([vx]))[0]), 7, episodes=500)
        r_catches.append(c)
    rng_t = np.random.default_rng(11)
    bx = rng_t.uniform(0.05, 0.95, 4096); vx = rng_t.uniform(-0.22, 0.22, 4096)
    Xt = np.stack([bx, vx, np.zeros_like(bx)], 1); yt = reflect01(bx + 4*vx).reshape(-1, 1)
    params = [rng_t.normal(0, 0.5, (3, 32)), np.zeros(32), rng_t.normal(0, 0.5, (32, 1)), np.zeros(1)]
    m = [np.zeros_like(p) for p in params]; v = [np.zeros_like(p) for p in params]
    for t in range(1, 1201):
        H = np.maximum(Xt @ params[0] + params[1], 0)
        out = H @ params[2] + params[3]
        d = (out - yt) / len(Xt) * 2
        dH = (d @ params[2].T) * (H > 0)
        grads = [Xt.T @ dH, dH.sum(0), H.T @ d, d.sum(0)]
        for i in range(4):
            m[i] = 0.9*m[i] + 0.1*grads[i]; v[i] = 0.999*v[i] + 0.001*grads[i]**2
            params[i] -= 0.01 * (m[i]/(1-0.9**t)) / (np.sqrt(v[i]/(1-0.999**t)) + 1e-8)
    tnet = tuple(params)
    fn_t = lambda bx, vx: float(net_target(tnet, np.array([bx]), np.array([vx]))[0])
    t_catch, t_mae = simulate_catch(fn_t, 7)
    t_catch_h, t_mae_h = simulate_catch(fn_t, 7, speed=0.16, window=0.04)
    return {"triangle_wave_max_error_reachable_range": tri_err,
            "written_catch_rate": w_catch, "written_target_mae": w_mae,
            "written_catch_rate_hard": w_catch_h, "written_target_mae_hard": w_mae_h,
            "written_gradient_steps": 0, "written_training_examples": 0,
            "random_catch_rate_mean": float(np.mean(r_catches)),
            "random_catch_rate_max": float(np.max(r_catches)),
            "trained_oracle_catch_rate": t_catch, "trained_oracle_target_mae": t_mae,
            "trained_oracle_catch_rate_hard": t_catch_h, "trained_oracle_target_mae_hard": t_mae_h,
            "trained_gradient_steps": 1200, "trained_examples": 4096, "episodes": 2000,
            "hard_regime": "paddle speed 0.16/tick, catch window 0.04"}

# ---------------------------------------------------------------- E3: FIX
def mc_step(x, v, a):
    v = float(np.clip(v + 0.001 * a - 0.0025 * math.cos(3 * x), -0.07, 0.07))
    x = x + v
    if x < -1.2: x, v = -1.2, 0.0
    return x, v

def run_policy(policy_fn, seed, episodes=512, max_steps=200):
    rng = np.random.default_rng(seed); wins = 0
    for _ in range(episodes):
        x = rng.uniform(-0.6, -0.4); v = 0.0
        for _ in range(max_steps):
            x, v = mc_step(x, v, policy_fn(x, v))
            if x >= 0.5: wins += 1; break
    return wins / episodes

def run_e3():
    rng = np.random.default_rng(21)
    states, acts = [], []
    for _ in range(400):
        x = rng.uniform(-0.6, -0.4); v = 0.0
        for _ in range(200):
            states.append([x, v]); acts.append(2)   # expert: always push right
            x, v = mc_step(x, v, 1)
            if x >= 0.5: break
    S = np.array(states); A = np.zeros((len(acts), 3)); A[np.arange(len(acts)), acts] = 1.0
    P = [rng.normal(0, math.sqrt(2/2), (2, 24)), np.zeros(24),
         rng.normal(0, math.sqrt(2/24), (24, 24)), np.zeros(24),
         rng.normal(0, math.sqrt(2/24), (24, 3)), np.zeros(3)]
    m = [np.zeros_like(p) for p in P]; vv = [np.zeros_like(p) for p in P]
    for t in range(1, 601):
        H1 = np.maximum(S @ P[0] + P[1], 0); H2 = np.maximum(H1 @ P[2] + P[3], 0)
        Z = H2 @ P[4] + P[5]; Z -= Z.max(1, keepdims=True)
        Pr = np.exp(Z); Pr /= Pr.sum(1, keepdims=True)
        dZ = (Pr - A) / len(S); g = [None]*6
        g[4] = H2.T @ dZ; g[5] = dZ.sum(0)
        dH2 = (dZ @ P[4].T) * (H2 > 0); g[2] = H1.T @ dH2; g[3] = dH2.sum(0)
        dH1 = (dH2 @ P[2].T) * (H1 > 0); g[0] = S.T @ dH1; g[1] = dH1.sum(0)
        for i in range(6):
            m[i] = 0.9*m[i] + 0.1*g[i]; vv[i] = 0.999*vv[i] + 0.001*g[i]**2
            P[i] -= 0.01 * (m[i]/(1-0.9**t)) / (np.sqrt(vv[i]/(1-0.999**t)) + 1e-8)
    def policy(P_):
        def f(x, v):
            h1 = np.maximum(np.array([x, v]) @ P_[0] + P_[1], 0)
            h2 = np.maximum(h1 @ P_[2] + P_[3], 0)
            return int(np.argmax(h2 @ P_[4] + P_[5])) - 1
        return f
    base_rate = run_policy(policy(P), 99)
    total_params = int(sum(p.size for p in P))

    # ---- surgical edit v2. Diagnosis: the imitated policy pushes right
    # regardless of velocity and stalls on the slope; the task is solvable
    # by energy pumping (push in the direction of motion). Construction:
    #  * rewrite the two least-used layer-1 units as exact velocity
    #    detectors p = ReLU(K v), q = ReLU(-K v);
    #  * rewire the two least-used layer-2 units as u0 ~ ReLU(p - q),
    #    u1 ~ ReLU(q - p) by setting two high-gain incoming weights each
    #    (residual incoming weights are left in place and are swamped);
    #  * point u0 at the "push right" logit and u1 at "push left".
    # At v = 0 both detectors are silent and the base policy starts the
    # car moving; once moving, the override pumps energy each swing.
    Q = [p.copy() for p in P]
    edited = set()
    def setv(pi, idx, val):
        if Q[pi][idx] != val: edited.add((pi, idx))
        Q[pi][idx] = val
    l1_cost = np.abs(Q[0]).sum(0) + np.abs(Q[2]).sum(1)
    det = list(np.argsort(l1_cost)[:2]); p_u, q_u = det
    K = 80.0
    setv(0, (0, p_u), 0.0); setv(0, (1, p_u), K);  setv(1, p_u, 0.0)
    setv(0, (0, q_u), 0.0); setv(0, (1, q_u), -K); setv(1, q_u, 0.0)
    l2_cost = np.abs(Q[2]).sum(0) + np.abs(Q[4]).sum(1)
    spare = [int(i) for i in np.argsort(l2_cost) if int(i) not in ()][:2]
    u0, u1 = spare; G, M = 6.0, 40.0
    setv(2, (p_u, u0), G);  setv(2, (q_u, u0), -G); setv(3, u0, -0.3)
    setv(2, (p_u, u1), -G); setv(2, (q_u, u1), G);  setv(3, u1, -0.3)
    setv(4, (u0, 2), M); setv(4, (u0, 0), -M); setv(4, (u0, 1), 0.0)
    setv(4, (u1, 0), M); setv(4, (u1, 2), -M); setv(4, (u1, 1), 0.0)
    n_edited = len(edited)
    fixed_rate = run_policy(policy(Q), 99)
    # control: same number of random edits
    R = [p.copy() for p in P]
    flat_idx = [(i, idx) for i, p in enumerate(P) for idx in np.ndindex(p.shape)]
    for pi_ in rng.choice(len(flat_idx), size=n_edited, replace=False):
        i, idx = flat_idx[int(pi_)]; R[i][idx] += rng.normal(0, 0.5)
    ctrl_rate = run_policy(policy(R), 99)
    # sensitivity to override output gain
    sens = {}
    for s in [0.0, 0.25, 0.5, 1.0, 2.0]:
        S_ = [p.copy() for p in P]
        for (pi, idx) in edited:
            if pi == 4: S_[4][idx] = P[4][idx] + s * (Q[4][idx] - P[4][idx])
            elif pi == 2: S_[2][idx] = s * Q[2][idx]
            elif pi == 0: S_[0][idx] = Q[0][idx]
            elif pi in (1, 3): S_[pi][idx] = Q[pi][idx]
        sens[str(s)] = run_policy(policy(S_), 99, episodes=256)
    return {"policy_params": total_params,
            "base_success_rate": base_rate,
            "edited_weights": n_edited,
            "edited_fraction_pct": round(100 * n_edited / total_params, 2),
            "fixed_success_rate": fixed_rate,
            "random_edit_control_success_rate": ctrl_rate,
            "override_sensitivity": sens, "episodes_eval": 512}

def main():
    t0 = time.time()
    summary = {"generated": "2026-11-03", "host": "Muse VM, NumPy CPU", "experiments": {}}
    for name, fn in [("E1_read", run_e1), ("E2_write", run_e2), ("E3_fix", run_e3)]:
        r = fn(); summary["experiments"][name] = r
        print(name, json.dumps(r, indent=1), flush=True)
    summary["wall_seconds"] = round(time.time() - t0, 1)
    (OUT / "summary_e123.json").write_text(json.dumps(summary, indent=1))
    print("wrote summary_e123.json in", summary["wall_seconds"], "s")

if __name__ == "__main__":
    main()
