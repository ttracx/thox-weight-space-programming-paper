"""Scoped loop baseline (whitepaper E4a/E4b, THOX-run, CPU).

Models: Qwen/Qwen3.5-0.8B (pinned rev) base vs RikiyaT edited, thinking
on; base with thinking OFF (the key decoding control); Thox-ai/
thox-micro-125m. Prompts: 8 hand-written gradeable math problems.
Metrics per run: cap-hit rate, loop rate (wsp.loopmetrics), mean tokens,
exact-answer accuracy. SMALL N: a baseline instrument check, not a
benchmark claim. Run: .venv-torch/bin/python exp/loop_baseline.py
"""
import json, sys, time
from pathlib import Path
import torch
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src" / "thox-wsp"))
from wsp.loopmetrics import summarize, is_loop

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "exp" / "results"
# Harder, multi-step problems chosen to give looping a chance to appear
# inside a CPU-feasible token budget (the source's loops were measured
# at a 32,768-token cap on MATH/GSM8K practice sets; this is a scoped
# instrument check, not that benchmark).
PROBLEMS = [
    ("How many trailing zeros does 100! have?", "25"),
    ("A sequence is defined by a_1 = 1 and a_(n+1) = 2*a_n + 3. What is a_10?", "2045"),
    ("What is the sum of all positive integers n <= 100 such that n and 100 are coprime?", "2000"),
    ("A fair coin is flipped until two consecutive heads appear for the first time. What is the expected number of flips?", "6"),
]
MAXNEW = 320

def run_model(name, loader, thinking=None, maxnew=MAXNEW):
    from transformers import AutoTokenizer
    tok, model = loader()
    recs, correct = [], 0
    for q, want in PROBLEMS:
        msgs = [{"role": "user", "content": q}]
        kw = {}
        if thinking is not None:
            kw["enable_thinking"] = thinking
        try:
            enc = tok.apply_chat_template(msgs, add_generation_prompt=True,
                                          return_tensors="pt", return_dict=True, **kw)
        except (TypeError, ValueError):
            # base models without a chat template (e.g. thox-micro-125m):
            # plain completion prompt
            enc = tok(f"Question: {q}\nAnswer:", return_tensors="pt")
        plen = enc["input_ids"].shape[1]
        with torch.no_grad():
            out = model.generate(**enc, max_new_tokens=maxnew, do_sample=True,
                                 temperature=0.6, top_p=0.95, top_k=20,
                                 pad_token_id=tok.eos_token_id)
        gen = out[0][plen:]
        text = tok.decode(gen, skip_special_tokens=True)
        hit_cap = len(gen) >= maxnew
        ok = want in text.split("boxed")[-1] if "boxed" in text else (text.strip().endswith(want) or f" {want}" in text[-60:])
        correct += int(ok)
        recs.append({"text": text, "hit_cap": hit_cap, "tokens": int(len(gen)), "correct": bool(ok)})
        print(f"  [{name}] tok={len(gen)} cap={hit_cap} loop={is_loop(text)} ok={ok}", flush=True)
    s = summarize(recs)
    s.update({"model": name, "accuracy": correct / len(PROBLEMS),
              "mean_tokens": sum(r["tokens"] for r in recs) / len(recs)})
    del model
    return s

def qwen_loader(repo, rev=None):
    def f():
        from transformers import AutoTokenizer, AutoModelForImageTextToText
        tok = AutoTokenizer.from_pretrained(repo, revision=rev)
        model = AutoModelForImageTextToText.from_pretrained(
            repo, revision=rev, dtype=torch.bfloat16)
        model.eval()
        return tok, model
    return f

def micro_loader():
    def f():
        from transformers import AutoTokenizer, AutoModelForCausalLM
        repo = "Thox-ai/thox-micro-125m"
        tok = AutoTokenizer.from_pretrained(repo)
        model = AutoModelForCausalLM.from_pretrained(repo, dtype=torch.float32)
        model.eval()
        return tok, model
    return f

def main():
    torch.set_num_threads(4)
    t0 = time.time(); results = []
    jobs = [
        ("qwen35-0.8b-base-thinking", qwen_loader("Qwen/Qwen3.5-0.8B", "2fc06364715b967f1860aea9cf38778875588b17"), True),
        ("qwen35-0.8b-base-nothink", qwen_loader("Qwen/Qwen3.5-0.8B", "2fc06364715b967f1860aea9cf38778875588b17"), False),
        ("qwen35-0.8b-edited-thinking", qwen_loader("RikiyaT/Qwen3.5-0.8B-weight-space-programming"), True),
    ]
    for name, loader, thinking in jobs:
        print(f"== {name}", flush=True)
        try:
            r = run_model(name, loader, thinking=thinking,
                          maxnew=MAXNEW if "micro" not in name else 384)
        except Exception as e:
            r = {"model": name, "error": f"{type(e).__name__}: {e}"}
            print("  ERROR", r["error"], flush=True)
        results.append(r)
    out = {"scope": "4 hand-written multi-step problems, CPU, temp 0.6/top-p 0.95/top-k 20, max_new 320; no presence penalty (transformers CPU generate); scoped instrument check, not a benchmark; micro measured separately in summary_loop_micro.json",
           "runs": results, "wall_seconds": round(time.time() - t0, 1)}
    (OUT / "summary_loop_baseline.json").write_text(json.dumps(out, indent=1))
    print(json.dumps(out, indent=1))

if __name__ == "__main__":
    main()
