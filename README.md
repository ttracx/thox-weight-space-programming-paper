# Weight-Space Programming for THOX Edge Models

**THOX.ai Research technical report v1.0.1 (public edition, 2026-11-04)**
Craig Ross (CEO) · Tommy Xaypanya (CTO & Co-Founder, corresponding author)
Zenodo DOI: [10.5281/zenodo.23954379](https://doi.org/10.5281/zenodo.23954379) · License: CC BY 4.0

Takehi et al. (MIT CSAIL, 2026-11-02) report that a frontier LLM can read
and write neural network weights directly, and that editing 0.016% of
Qwen3.5-0.8B's weights raised MATH-500 from 7.9% to 48.1% by removing a
thinking-loop failure. THOX ships a derivative of that exact base model,
so we reviewed the claim, recreated its three verbs at checkable scale,
verified the released artifact ourselves, and built the infrastructure
the method needs if it is ever to ship.

Headline results (all THOX-measured, evidence in `artifact/exp/results/`):

- **E0 verification, PASS.** The released edit rebuilds bit-exactly:
  130,188 entries changed, both tensor SHA-256 values match the
  published ones, each diff rank-1 at 99.999% of energy.
- **Read.** Task identity is legible in composed per-class circuits
  (100% reader accuracy) and illegible in layer marginals (chance).
- **Write.** A hand-written control network matches an oracle-trained
  one exactly (zero gradient steps).
- **Fix.** 16 of 747 weights repair a policy stuck at 0% (92.8%
  success, random-edit control 0%).
- **Audit.** A clean negative: the induction behaviour never emerged
  in training, so there was nothing to audit. Reported in full.
- **Patch channel.** `thox-wsp` v0.1.0: Ed25519-signed, base-hash-pinned
  rank-1 manifests (factor form ~4.4 KB against a 529 MB full-model
  re-issue), Python toolkit, Rust loader with A/B rollback,
  cross-language end-to-end test passing. Also carries LoRA and
  distillation deltas.

Adoption bar set by the paper: a THOX weight patch ships only when it
beats the best decoding-only control by more than two standard errors,
with no retention regression. Adopt narrowly now; patch later, if it
earns it.

## Repository map

- `paper/` the shipped edition: PDF, single-file HTML, interactive demo.
- `artifact/` the reproducibility bundle: experiment code and results
  (`exp/`, with `exp/results/summary.json` as the single evidence
  source), paper build sources and QA (`wp/`).
- `docs/` user guide, quickstart, development notes, previews.
- `CITATION.cff`, `paper.bib` (in `artifact/` build tree) citation files.
- `.agents/HANDOFF.md` the publication record: hashes, consent status,
  edition history.

The patch-channel source ships inside `artifact/src/thox-wsp/` in this
edition (Python toolkit, Rust loader, tests).

## Cite

Ross, C., & Xaypanya, T. (2026). *Weight-Space Programming for THOX
Edge Models: Evidence Review, Small-Scale Recreation, and a Signed
Patch Channel* (v1.0.1). THOX.ai Research. https://doi.org/10.5281/zenodo.23954379
