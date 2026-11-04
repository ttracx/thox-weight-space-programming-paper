"""Standalone thox-micro-125m loop baseline (the main script's micro job
predates the chat-template fallback). Same problems/metrics as
loop_baseline.py; writes summary_loop_micro.json."""
import json, sys, time
from pathlib import Path
import torch
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src" / "thox-wsp"))
from wsp.loopmetrics import summarize, is_loop
from loop_baseline import PROBLEMS

from transformers import AutoTokenizer, AutoModelForCausalLM
repo = "Thox-ai/thox-micro-125m"
tok = AutoTokenizer.from_pretrained(repo)
model = AutoModelForCausalLM.from_pretrained(repo, dtype=torch.float32); model.eval()
recs, correct = [], 0
for q, want in PROBLEMS:
    enc = tok(f"Question: {q}\nAnswer:", return_tensors="pt")
    with torch.no_grad():
        out = model.generate(**enc, max_new_tokens=384, do_sample=True,
                             temperature=0.6, top_p=0.95, top_k=20,
                             pad_token_id=tok.eos_token_id)
    gen = out[0][enc["input_ids"].shape[1]:]
    text = tok.decode(gen, skip_special_tokens=True)
    ok = text.strip().endswith(want) or f" {want}" in text[-60:]
    correct += int(ok)
    recs.append({"text": text, "hit_cap": len(gen) >= 384, "tokens": int(len(gen)), "correct": bool(ok)})
    print(f"  [micro] tok={len(gen)} cap={len(gen)>=384} loop={is_loop(text)} ok={ok}", flush=True)
s = summarize(recs)
s.update({"model": "thox-micro-125m", "accuracy": correct / len(PROBLEMS),
          "mean_tokens": sum(r["tokens"] for r in recs) / len(recs),
          "note": "plain completion prompt; the model ships no chat template"})
Path("exp/results/summary_loop_micro.json").write_text(json.dumps(s, indent=1))
print(json.dumps(s, indent=1))
