# QA report: Weight-Space Programming for THOX Edge Models, v1.0.0 (internal edition)

Date: 2026-11-03. Builder: Sadie Weaving (CAO office). Validator: independent
script (wp/validate.py) + visual inspection; the validator does not import
the build code.

## Independent validation (wp/validate.py): ALL PASS (23 checks)
- E0 totals, both edited-tensor SHA-256 values (match published), E1 reader
  accuracies (R4 100%, R1-R3 at chance), E2 written == trained catch rate,
  E3 fraction/success/control, E4 repeat loss at the ln(24) floor, patch-size
  arithmetic: all re-derived from exp/results/summary.json and found in the
  paper text as stated.
- Blocker sweep clean: no placeholders, no internal file paths, no
  disclosure labels, all 31 citations resolve to the reference list, both
  authors on the cover with roles, names not split across lines.
- Demo: self-contained (no external resources), carries the E0 total.

## Visual inspection
- Paper PDF (20 pp, A4): cover inspected (fits one page; eyebrow, pill,
  title, deck, byline with roles, abstract, two-column contents all
  present and legible); KPI cards inspected in the light body (readable,
  evidence-class tags present); body pages 3, 4 and 9 inspected (tables,
  callouts, figure placement, citation rendering all correct). Full
  20-page contact sheet: wp/figures/qa-contact-sheet.png.
- Demo HTML: the managed Chromium on this host refuses headless startup
  (WebGL domain policy) and the browser tool cannot open file:// URLs,
  so no pixel screenshot of the demo exists. Substituted checks, all
  passing: JavaScript syntax (node --check), every getElementById target
  present in the DOM, data blocks present, template CSS unmodified from
  the canonical demo template. A rendered-frame pass on the demo is owed
  before any public posting of it.

## Known open item
- Scoped loop baseline (exp/loop_baseline.py + exp/micro_loop.py) still
  running on CPU reference kernels at pack time. The paper's Section 5
  carries the measurement-status callout; no claim depends on it. When
  summary_loop_baseline.json lands, rebuild with wp/build.py +
  wp/build_demo.py + wp/render.py and re-issue as v1.0.1 internal.

## v1.0.1 public edition (2026-11-04)
- wp/validate.py re-run on the v1.0.1 rebuild: ALL PASS (23/23).
- Cover page rendered and visually inspected: "Public edition" pill,
  technical report v1.0.1, 2026-11-04, DOI 10.5281/zenodo.23954379 in
  the cover foot, author names and roles intact.
- Demo rebuilt with micro loop-baseline data; syntax/DOM checks from
  v1.0.0 still owed a rendered-frame pass before social use.
