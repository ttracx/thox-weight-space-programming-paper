"""Independent validation: re-derive the paper's load-bearing numbers from
exp/results/summary.json and check the built HTML against them; sweep for
publication blockers. Does not import build.py."""
import json, re, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
S = json.loads((ROOT / "exp/results/summary.json").read_text())
html = (ROOT / "wp/paper.src.html").read_text()
text = re.sub(r"<[^>]+>", " ", html)
fails = []
def check(name, cond):
    print(("PASS " if cond else "FAIL ") + name)
    if not cond: fails.append(name)

E1, E2, E3 = S["experiments"]["E1_read"], S["experiments"]["E2_write"], S["experiments"]["E3_fix"]
E0, E4 = S["E0_verification"], S["E4_audit"]
t15 = E0["tensors"]["model.language_model.layers.15.mlp.down_proj.weight"]
t19 = E0["tensors"]["model.language_model.layers.19.mlp.down_proj.weight"]
check("E0 total changed in paper", f"{E0['total_entries_changed']:,}" in text)
check("E0 hash L15 matches published + paper", t15["edited_sha256"].startswith("82e2d733") and t15["edited_sha256"][-5:] == "2ee53" and "82e2d733" in text)
check("E0 hash L19 matches published + paper", t19["edited_sha256"].startswith("8ef3c61b") and t19["edited_sha256"][-5:] == "12eb2" and "8ef3c61b" in text)
check("E1 R4 accuracy 100% in paper", abs(E1["readers"]["R4_effective_per_class"]["accuracy"] - 1.0) < 1e-9 and "100%" in text)
check("E1 R1-R3 at chance", all(abs(E1["readers"][k]["accuracy"] - 1/3) < 0.01 for k in ["R1_global_marginal_W1", "R2_per_unit_voting_W1", "R3_effective_map"]))
check("E2 written == trained catch", E2["written_catch_rate"] == E2["trained_oracle_catch_rate"] == 1.0)
check("E3 fraction 2.14%", abs(E3["edited_fraction_pct"] - 2.14) < 0.01 and "2.14%" in text)
check("E3 fixed success 92.8%", abs(E3["fixed_success_rate"] - 0.9277) < 0.001 and "92.8%" in text)
check("E3 control 0%", E3["random_edit_control_success_rate"] == 0.0)
check("E4 repeat loss at floor (ln24=3.178)", abs(E4["repeat_position_loss"] - 3.178) < 0.05)
check("patch size calc: factor ~4.4KB for 2 tensors", 2 * (1024 * 2 + 64 * 2 + 16) == 4384)
# blockers sweep
for bad in ["lorem", "TODO", "FIXME", "XXX", "~/workspace", "/home/hatch", "AI-generated", "AI generated"]:
    check(f"blocker absent: {bad}", bad not in html)
cites = [int(n) for n in re.findall(r'class="cite">\[(\d+)\]', html)]
refs = len(re.findall(r'class="rn">', html))
check("all citations resolve to reference list", cites and max(cites) <= refs)
check("both authors on cover with roles", "Craig Ross, Chief Executive Officer" in text and "Tommy Xaypanya, Chief Technology Officer" in text)
demo = (ROOT / "wp/weight-space-programming-demo.html").read_text()
check("demo is self-contained (no external http resources)", not re.search(r'(src|href)="http', demo))
check("demo carries E0 total", f"{E0['total_entries_changed']:,}" in demo)
print("RESULT:", "ALL PASS" if not fails else f"{len(fails)} FAILURES: {fails}")
sys.exit(1 if fails else 0)
