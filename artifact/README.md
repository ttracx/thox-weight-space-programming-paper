# Weight-Space Programming for THOX Edge Models: artifact bundle

Paper: THOX.ai Research technical report v1.0.1 (public edition, 2026-11-04).
Zenodo DOI: 10.5281/zenodo.23954379 (CC BY 4.0). First issued internally
as v1.0.0 on 2026-11-03.
Authors: Craig Ross (CEO); Tommy Xaypanya (CTO & Co-Founder, corresponding).

## Contents
- `dist/` the shipped files: paper PDF, single-file paper HTML, DOCX,
  interactive demo HTML.
- `exp/` experiment code and results. `exp/results/summary.json` is the
  single evidence source for every number in the paper; `exp/FINDINGS_V1.md`
  preserves the failed iterations (readers v1/v2, edit v1).
- `src/thox-wsp/` the patch channel: Python toolkit (`wsp/`), Rust loader
  (`rust/thox-patch-loader/`), end-to-end test (`tests/`).
- `wp/` paper build (`build.py`, `build_demo.py`, `render.py`,
  `validate.py`), figures and QA report.
- `CITATION.cff`, `paper.bib` citation files. `HANDOFF.md` publication
  record with SHA-256 hashes and consent status.

## Reproduce
- Experiments: `python3 exp/wsp_experiments.py`, `.venv-torch/bin/python
  exp/wsp_e4_audit.py`, `.venv-torch/bin/python exp/e0_rebuild.py`
  (downloads the pinned tensors), `exp/loop_baseline.py` (scoped, slow on
  CPU reference kernels).
- Patch channel: `cd src/thox-wsp/rust/thox-patch-loader && cargo test
  --offline`, then `python3 src/thox-wsp/tests/test_patch_channel_e2e.py`.
- Paper: `python3 wp/build.py && python3 wp/build_demo.py`, render with
  the typesetting venv python: `wp/render.py`. Validate: `wp/validate.py`.

## Status
Public edition v1.0.1, published on the CTO's order (2026-11-04) under
the THOX Research Paper Process v1.0 and deposited at Zenodo,
DOI 10.5281/zenodo.23954379. Co-author consent record: see HANDOFF.md.
