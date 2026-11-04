# Data Supplement S1 — Scoped loop baseline (companion to WSP paper v1.0.1)

Paper: "Weight-Space Programming for THOX Edge Models" (Ross &
Xaypanya, THOX.ai Research v1.0.1, DOI 10.5281/zenodo.23954379).
This supplement completes the Section 5 measurement-status item. It
does not change any claim in the paper.

## Instrument
Four hand-written multi-step problems (factorial trailing zeros,
recurrence, coprime sum, consecutive-heads expectation). Sampling:
temperature 0.6, top-p 0.95, top-k 20 (the source's profile family),
no presence penalty. Qwen arms: max 320 new tokens, KnightHub RTX
4060 Ti (GPU rerun 2026-11-04 after the CPU runs on the build VM did
not complete). thox-micro-125m arm: plain completion (the model ships
no chat template), max 384 tokens, CPU. Loop test: the paper's strict
detector (a repeated 8-gram covering >= 90% of a 300-token window).

## Results (n = 4 per configuration)
| Configuration | Cap-hit | Strict loop | Accuracy | Mean tokens |
|---|---|---|---|---|
| Qwen3.5-0.8B base, thinking on | 100% | 0% | 0% | 320 |
| Qwen3.5-0.8B base, thinking off | 100% | 0% | 0% | 320 |
| Qwen3.5-0.8B released edit, thinking on | 100% | 0% | 0% | 320 |
| thox-micro-125m (plain completion) | 100% | 0% | 0% | 384 |

Raw files: exp/results/summary_loop_baseline.json (Qwen arms, wall
399.4 s on GPU) and exp/results/summary_loop_micro.json, merged into
exp/results/summary.json.

## Reading
At a 320-token budget on these four problems, nothing terminates in
any configuration, the strict loop detector never fires, and the
instrument distinguishes nothing: neither the edit nor the
thinking-off control shows an effect at this scale. This bounds the
scoped check, it does not test the source's result, which was measured
at a 32,768-token cap on MATH-500/GSM8K practice sets. The deciding
comparison remains the Section 8 E4 protocol on GPU benchmark runs.
