"""Figures for the THOX WSP whitepaper. Every number comes from
exp/results/summary*.json (generated before the loop baseline finished;
loop figure is added by build.py when summary_loop_baseline.json exists).
Run: python3 wp/figures.py  -> wp/figures/*.png (200 dpi)."""
import json
from pathlib import Path
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

ROOT = Path(__file__).resolve().parents[1]
FIG = ROOT / "wp" / "figures"; FIG.mkdir(parents=True, exist_ok=True)
GREEN = "#05A451"; INK = "#09090B"; GRAY = "#8a8a8a"
plt.rcParams.update({"font.family": "DejaVu Sans", "text.color": INK,
                     "axes.edgecolor": GRAY, "axes.labelcolor": INK,
                     "xtick.color": INK, "ytick.color": INK, "font.size": 9})
S123 = json.loads((ROOT / "exp/results/summary_e123.json").read_text())["experiments"]
E0 = json.loads((ROOT / "exp/results/summary_e0.json").read_text())

def save(fig, name):
    fig.tight_layout(); fig.savefig(FIG / name, dpi=200); plt.close(fig)
    print("wrote", name)

# F1: E1 readers
r = S123["E1_read"]["readers"]
names = ["R1\nglobal marginal", "R2\nper-unit voting", "R3\neffective map", "R4\neffective per-class"]
accs = [r[k]["accuracy"] for k in ["R1_global_marginal_W1", "R2_per_unit_voting_W1", "R3_effective_map", "R4_effective_per_class"]]
fig, ax = plt.subplots(figsize=(6.4, 3.2))
bars = ax.bar(names, accs, color=[GRAY, GRAY, GRAY, GREEN])
ax.axhline(1/3, color=INK, ls="--", lw=1); ax.text(3.45, 0.36, "chance", ha="right", fontsize=8)
ax.set_ylabel("task-identification accuracy (30 networks)")
ax.set_ylim(0, 1.12); ax.set_title("Figure 1. Reading task identity from weights: only the per-class composed reader works", fontsize=9, loc="left")
for b, a in zip(bars, accs): ax.text(b.get_x() + b.get_width()/2, a + 0.03, f"{a:.0%}", ha="center")
save(fig, "fig1_readers.png")

# F2: E2 write
e2 = S123["E2_write"]
fig, ax = plt.subplots(figsize=(6.4, 3.2))
labels = ["Written\n(0 steps)", "Trained on oracle\n(1,200 steps)", "Random\n(mean of 20)"]
std = [e2["written_catch_rate"], e2["trained_oracle_catch_rate"], e2["random_catch_rate_mean"]]
hard = [e2["written_catch_rate_hard"], e2["trained_oracle_catch_rate_hard"], 0.0]
x = np.arange(3)
ax.bar(x - 0.2, std, 0.4, color=GREEN, label="standard regime")
ax.bar(x + 0.2, hard[:2] + [np.nan], 0.4, color=INK, label="hard regime (slower paddle, tighter window)")
ax.set_xticks(x); ax.set_xticklabels(labels); ax.set_ylim(0, 1.12)
ax.set_ylabel("catch rate (2,000 episodes)")
ax.legend(frameon=False, fontsize=8)
ax.set_title("Figure 2. A hand-written network matches an oracle-trained one; both are paddle-limited in the hard regime", fontsize=9, loc="left")
save(fig, "fig2_write.png")

# F3: E3 fix sensitivity
e3 = S123["E3_fix"]
sens = e3["override_sensitivity"]
xs = [float(k) for k in sens]; ys = [sens[k] for k in sens]
fig, ax = plt.subplots(figsize=(6.4, 3.2))
ax.plot(xs, ys, marker="o", color=GREEN, lw=2)
ax.axhline(e3["base_success_rate"], color=INK, ls="--", lw=1)
ax.text(1.95, 0.03, "before edit: 0%", ha="right", fontsize=8)
ax.set_xlabel("override gain (1.0 = the shipped edit, 16 of 747 weights = 2.14%)")
ax.set_ylabel("MountainCar success (256 episodes)")
ax.set_ylim(-0.03, 1.05)
ax.set_title("Figure 3. Sparse surgical fix: success rises with override gain; random edits of the same size stay at 0%", fontsize=9, loc="left")
save(fig, "fig3_fix.png")

# F4: E0 rank-1 evidence
fig, ax = plt.subplots(figsize=(6.4, 3.0))
layers = ["layer 15\ndown_proj", "layer 19\ndown_proj"]
ratios = [E0["tensors"][k]["sv_ratio_s1_over_s2"] for k in E0["tensors"]]
changed = [E0["tensors"][k]["entries_changed_bitwise"] for k in E0["tensors"]]
ax2 = ax.twinx()
ax.bar([0, 1], ratios, 0.45, color=GREEN)
ax.set_xticks([0, 1]); ax.set_xticklabels(layers)
ax.set_ylabel("singular-value ratio sigma1/sigma2 of the diff")
ax2.bar([0.55, 1.55], changed, 0.3, color=INK)
ax2.set_ylabel("entries changed bitwise (bf16)")
ax.set_title("Figure 4. THOX E0 verification: the released edit is rank-1 (sigma ratio > 1,500) in both tensors", fontsize=9, loc="left")
save(fig, "fig4_e0.png")

# F5: source Exp 8 headline (AUTHOR-REPORTED, labelled in the paper)
fig, ax = plt.subplots(figsize=(6.4, 3.2))
cats = ["MATH-500", "GSM8K", "IFEval"]
base = [7.9, 13.8, 21.0]; edited = [48.1, 67.1, 62.3]
x = np.arange(3)
ax.bar(x - 0.2, base, 0.4, color=GRAY, label="base (author-reported)")
ax.bar(x + 0.2, edited, 0.4, color=GREEN, label="edited, 50 passes (author-reported)")
ax.set_xticks(x); ax.set_xticklabels(cats); ax.set_ylim(0, 75)
ax.set_ylabel("accuracy %")
ax.legend(frameon=False, fontsize=8)
ax.set_title("Figure 5. Experiment 8 headline results as reported by Takehi et al. (not THOX measurements)", fontsize=9, loc="left")
save(fig, "fig5_exp8.png")
print("figures done")
