"""E0: rebuild the released Exp 8 edit bit-exactly.
Downloads ONLY the two edited tensors' shards from base (pinned rev)
and edited repos, factors the diff, checks rank-1 structure, touched
count, and sha256 of the edited tensors."""
import json, hashlib
from pathlib import Path
import numpy as np
from huggingface_hub import hf_hub_download, list_repo_files
from safetensors import safe_open

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "exp" / "results"
BASE = "Qwen/Qwen3.5-0.8B"; BASE_REV = "2fc06364715b967f1860aea9cf38778875588b17"
EDIT = "RikiyaT/Qwen3.5-0.8B-weight-space-programming"
TARGETS = ["model.language_model.layers.15.mlp.down_proj.weight",
           "model.language_model.layers.19.mlp.down_proj.weight"]

def load_tensor(repo, rev, name):
    files = list_repo_files(repo, revision=rev)
    idx = [f for f in files if f.endswith("model.safetensors.index.json")]
    shard = None
    if idx:
        p = hf_hub_download(repo, idx[0], revision=rev)
        mapping = json.loads(Path(p).read_text())["weight_map"]
        shard = mapping[name]
    else:
        shard = "model.safetensors"
    p = hf_hub_download(repo, shard, revision=rev)
    import torch
    with safe_open(p, framework="pt") as f:
        t = f.get_tensor(name)
    return t, p

res = {"base_rev": BASE_REV, "tensors": {}}
for name in TARGETS:
    import torch
    b, _ = load_tensor(BASE, BASE_REV, name)
    e, _ = load_tensor(EDIT, None, name)
    sha_e = hashlib.sha256(e.contiguous().view(torch.int16).numpy().tobytes()).hexdigest()
    sha_b = hashlib.sha256(b.contiguous().view(torch.int16).numpy().tobytes()).hexdigest()
    diff = (e.float() - b.float()).numpy()
    touched = int((e != b).sum().item())
    s = np.linalg.svd(diff, compute_uv=False)
    res["tensors"][name] = {
        "shape": list(e.shape), "dtype": str(e.dtype),
        "edited_sha256": sha_e, "base_sha256": sha_b,
        "entries_changed_bitwise": touched,
        "entries_total": int(e.numel()),
        "sv_ratio_s1_over_s2": float(s[0] / s[1]) if len(s) > 1 else None,
        "energy_rank1_pct": float(100 * s[0]**2 / (s**2).sum()),
        "rel_change_frobenius_pct": float(100 * np.linalg.norm(diff) / np.linalg.norm(b.float().numpy())),
    }
    print(name, json.dumps(res["tensors"][name], indent=1), flush=True)
res["total_entries_changed"] = sum(t["entries_changed_bitwise"] for t in res["tensors"].values())
(OUT / "summary_e0.json").write_text(json.dumps(res, indent=1))
print("TOTAL CHANGED", res["total_entries_changed"])
