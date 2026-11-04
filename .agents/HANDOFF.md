# HANDOFF: Weight-Space Programming for THOX Edge Models

## Edition of record (internal, 2026-11-03)
| File | SHA-256 |
|---|---|
| dist/Weight-Space-Programming-for-THOX-Edge-Models_v1.0.0.pdf | ff170419595f3effd1a82c959a79d3646b7ffcaa8d696d34766a5baa7e917a5c |
| dist/Weight-Space-Programming-for-THOX-Edge-Models_v1.0.0.html | 159dfb5fb90e4e3253cacc0f23220543e658f48b060e625ec32953bd2938957e |
| dist/Weight-Space-Programming-for-THOX-Edge-Models_v1.0.0.docx | 9cdd7726c3ddd1cf42fb30351ecc49946360c6abd4148e3184e8eee16ea5f4de |
| dist/weight-space-programming-demo.html | d6fec7f46b4f59f2f86981a4d96e6b012e58c0d718bab47bd250267664adf08e |

Paper: 20 pages, A4, ~8,260 words, 31 references (all arXiv entries
verified on their abstract pages by the literature lane, 2026-11-03).

## Public edition v1.0.1 (2026-11-04)

Published on Tommy Xaypanya's order (2026-11-04 08:54 CT: "Publish and
prepare announcements and updates to our website and so on"), following
the MeshStack v1.0.1 precedent (association pass proceeded on the CTO's
order with co-author consent outstanding). Craig Ross's written consent
to the exact bytes had NOT been received when publication was ordered
(verified 2026-11-04 ~08:57 CT: no reply to the 2026-11-03 delivery
email or to any of the three outstanding THOX paper consent asks).
Consent to these exact v1.0.1 bytes is requested in the founder closeout
of 2026-11-04 and its reply will be appended here when received.

Changes from v1.0.0: edition record only (public-edition pill and
cover-foot with the DOI, document-control status row), the Section 5
measurement-status update (micro arm landed: thox-micro-125m cap-hit
100%, strict-loop 0%, accuracy 0% at n=4; Qwen arms rerouted to a GPU
host, table to follow as a data supplement), and citation metadata
(CITATION.cff / paper.bib carry the DOI). No result, figure or
conclusion changed. Validation re-run: wp/validate.py ALL PASS (23/23).
Cover visually inspected (Public edition pill, v1.0.1, DOI line).

| File | SHA-256 |
|---|---|
| dist/Weight-Space-Programming-for-THOX-Edge-Models_v1.0.1.pdf | dfea8a7e401841f7a253d96847a7346cd31564daabce08b72a07aa985ff62723 |
| dist/Weight-Space-Programming-for-THOX-Edge-Models_v1.0.1.html | c38a99a64554b43cac1c88a253cba5f22659fc945f86868420e15e3119c70854 |
| dist/Weight-Space-Programming-for-THOX-Edge-Models_v1.0.1.docx | 0010c5fe69ed90eb7c096c92e3f7c11bc7f83fe5da91b4fda3bc75d03196089e |
| dist/weight-space-programming-demo.html | 399d4706eeaa67829d0afd7d3d0b68a153e6222428f937f704237070094b4d21 |

Zenodo: DOI 10.5281/zenodo.23954379 (concept DOI
10.5281/zenodo.23954378). PUBLISHED and verified anonymously
2026-11-04: record https://zenodo.org/records/23954379 carries the
PDF, HTML, demo and artifact ZIP, license CC BY 4.0, creators Ross
(ORCID 0009-0005-9872-3673) then Xaypanya (ORCID
0009-0000-4425-9565), version field 1.0.1 (set via the API edit cycle
after the browser publish).

Association pass (2026-11-04, one pass):
- GitHub: ttracx/thox-weight-space-programming-paper, public, release
  v1.0.1 with the paper trio; collaborator invites pending for
  sadiethox and cross80127 (push, the personal-repo maximum).
- Website: thox.ai PR #490 merged 2026-11-04; page live at
  /research/papers/weight-space-programming; hosted PDF and demo
  hash-match this edition (dfea8a7e... and 399d4706...); papers index
  carries the entry (7 papers).
- Hugging Face: Thox-ai/thox-whitepapers folder
  weight-space-programming/ (PDF + HTML) and a dataset-card entry
  with the DOI; status appended when the upload verifies.
- Pipeline: registered in ~/workspace/research-publishing-pipeline
  (registry.json + manifests/weight-space-programming.json).
- Data supplement S1 (scoped loop baseline, GPU run): pub/
  LOOP-BASELINE-SUPPLEMENT.md and repo docs/.
- Announcements: pub/ANNOUNCEMENTS.md (LinkedIn + X drafts). NOT
  posted; posting is the founders' call.

## What was done (per Tommy's order, 2026-11-03 11:32 CT, and Claude's
review + narrow-adoption plan, 12:08 CT)
1. Source reviewed in full (blog recovered past the truncated PDF;
   Experiments 7-8 and the Gemma control restored to the record).
2. THOX device context established from the live catalog: ThoxEdge-0.8B
   is a Qwen/Qwen3.5-0.8B derivative (GATE49 46/49, promoted, Mini
   routing model), served thinking-off today.
3. Recreation experiments run for real (exp/results/summary.json):
   E1 read (R4 per-class composed reader 100%; R1-R3 at chance), E2 write
   (hand-written network exact, matches oracle-trained), E3 fix (16/747
   weights, 0% to 92.8%, control 0%), E4 audit (negative: behaviour never
   emerged; reported in full).
4. E0 (Claude plan step 1): released Qwen3.5-0.8B edit verified
   bit-exactly on THOX infrastructure: 130,188 entries changed, both
   tensor SHA-256 match published values, both diffs rank-1 (99.999%).
5. Patch channel built (Claude plan step 3): thox-wsp v0.1.0, Python
   toolkit + Rust loader (Ed25519 manifest signing, base-hash pinning,
   A/B rollback); Rust tests 3/3; cross-language end-to-end ALL PASS
   (apply bit-identical, tamper rejected, wrong base aborted).
6. Paper + demo built in Template v1.0, validated independently
   (23/23 checks), visual QA on the PDF (contact sheet in wp/figures/).

## Open items (owned, with unblock conditions)
- Scoped loop baseline (Claude plan steps 1-2): still running on CPU
  reference kernels at pack time (exp/loop_baseline.py, exp/micro_loop.py).
  Paper Section 5 carries a measurement-status callout; no claim depends
  on it. On completion: rebuild and re-issue as internal v1.0.1.
- Demo rendered-frame QA: blocked on this host (managed Chromium policy;
  browser tool cannot open file://). Syntax/DOM/data checks pass. Do the
  pixel pass on a Mac before any public posting of the demo.
- E1'/E2' frontier-editor runs and the E4/E5 gated protocol (paper
  Section 8): not started; they are the follow-on research program.

## Consent and publication status
- Internal edition. Founder consent to exact bytes: NOT YET SOUGHT.
  This pack is delivered to both founders for review (closeout email).
- No Zenodo deposit, no arXiv submission, no HF Papers, no website page,
  no social posts. "Public release" steps each require the named
  edition's consent under the THOX Research Paper Process v1.0.
- No repository visibility changed; thox-wsp source ships inside this
  bundle only.

## Distribution
- Closeout [THOX Report] email SENT 2026-11-03 13:03 CT to tommy@thox.ai
  and craig@thox.ai via the Mac Graph route (TX083 mailer retired),
  HTTP 202 acceptance, VERIFIED in Sent Items (attachments present).
  PDF + DOCX attached; demo HTML not attached (thox.ai attachment policy).
- SharePoint archive copy (THOX Agent Reports Archive / Weight-Space
  Programming Paper / 2026-11) + Teams 1:1 pointer to Craig with the PDF
  attached in-thread: attempted via browser task 2026-11-03 ~13:05 CT;
  the browser lost its connection to SharePoint before any step
  completed. NO folder was created, NO files uploaded, NO Teams message
  sent. Both items remain open; the email delivery (above) is unaffected
  and Craig has the paper PDF and DOCX as attachments.
- Bundle location: ~/workspace/weight-space-programming-20261103/ and
  the artifact ZIP beside it.

## v1.1.0 public edition (2026-11-04)

Built by the Claude lane as an internal edition (THOX.ai Research
byline only, AI-assistance note in document control, Section 5 full
protocol unmeasured after HF Jobs returned 402). Tommy ruled
2026-11-04 09:47 CT: restore the Craig Ross + Tommy Xaypanya byline,
drop the AI note, publish as the public edition. Sadie rebuilt from
the lane's build sources on KnightHub (wp/build.py, pdf.cjs,
merge_pdf.py, demo_build.py): founder byline + roles restored,
AI-assistance row removed, public-edition pill and running footers,
Zenodo DOI baked into the cover foot and document control, change log
records the byline restoration. QA: 21 pages, cover inspected,
text-layer checks pass (no AI-assistance text; "internal edition"
survives only in the v1.0.0 reference entry).

SHA-256: PDF 5a44eeb60ef5836553c725bfdfacc1a60ef9e26708060f1e2c857a8d1ce94f4a;
HTML 059748917e83da2aba1435d1f2a79d340672ecf7f3984b5243e56eda722aaf50;
demo 88a08f0ae68737e77add61af59133f3fc0c673b882311420d004e87814857cb0;
artifact ZIP 3fe597562f7a69b6bbfac996d780e75e27a52c17fedb6bc6c08371b4378b45b3.

Zenodo: new version of record 23954379, DOI 10.5281/zenodo.23955394
(concept 10.5281/zenodo.23954378), published and hash-verified live.
GitHub: release v1.1.0 on ttracx/thox-weight-space-programming-paper
(trio + artifact ZIP); README updated. Website: PR #493 merged;
hosted v1.1.0 PDF/demo hash-match canonical; stat card corrected to
the 80.6 KB exact patch. Content deltas over v1.0.1: E0-R second-host
re-verification, P1 exact-patch correction (factor form exact on
118,160 of 130,188 entries; +12,028-entry residual = 80.6 KB vs the
released 387.6 KB sparse file), A0 paired analysis (edit higher on
306 MATH-500 problems, lower on none; AMC23 0.5% to 23.4%), Section 5
full protocol pre-registered (run stopped by HF billing 402; no
number stated; scoped S1 supplement stands), 47 references
re-verified (9 corrected), demo runs the real loop detector (6/6).

Founder comms: the Claude lane sent its own v1.1.0 report email
2026-11-04 09:42 CT from Sadie@thox.ai (no attachments). Sadie's
consolidated publication closeout follows separately and carries the
consent request for the exact v1.1.0 bytes above. Craig's consent:
outstanding at publication (Tommy's CTO order), as with v1.0.1.

## Reconciliation, Claude lane (2026-11-04, after the v1.1.0 publication)

Two different byte sets were labeled v1.1.0 for about 20 minutes. Record
of each, kept separate:

- **Record (canonical).** Sadie's rebuild per Tommy's 09:47 CT ruling:
  founder byline, no AI-assistance row, Zenodo DOI 10.5281/zenodo.23955394.
  PDF 5a44eeb6...; HTML 05974891... This is v1.1.0.
- **Claude-lane candidate (not published, superseded).** Built 09:56 CT in
  the Claude workspace before the ruling reached that lane: THOX.ai
  Research byline, AI-assistance row kept, plus the deltas below. PDF
  e012202e5f35...; HTML 7a57de0c41c9...; demo 21956efa43ea.... Its
  website branch was never merged; it is not a THOX edition and must not
  be cited as v1.1.0.

Deltas from the candidate that are queued for v1.1.1 (none changes a
v1.1.0 conclusion):
1. E1 to E3 re-run on a second host (Claude cloud workspace, CPU,
   Python 3.12, NumPy 2.5.3) from `artifact/exp/wsp_experiments.py`
   with the weight cache removed: 50 of 54 recorded values identical;
   the oracle-trained MAE differs at 4.6e-7 relative (two copies), the
   triangle-wave reachable-range error is 2.2e-16 vs 4.4e-16 (machine
   epsilon), and wall time differs. Evidence:
   `artifact/exp/results/rerun_e123_second_host.json` and
   `summary_e123_rerun_second_host.json`. E4 (PyTorch) not re-run.
2. Patch-channel tests re-run on the same host: Rust `cargo test` 3/3,
   `tests/test_patch_channel_e2e.py` ALL PASS.
3. Section 5 note on the v1.0.1 S1 supplement (320-token cap, every arm
   capped, loop detector never fired: the instrument distinguished
   nothing at that budget).
4. Carried-number cross-check against `artifact/exp/results/summary.json`
   (14 values match).

Website: thox.ai commit b50a3db (main, 2026-11-04) aligned the v1.1.0
page with the record. The page had shown the v1.0.1 abstract, v1.0.1
stat cards and Section 5 title, the v1.0.1 DOI under "DOI record", and a
Hugging Face link: Thox-ai/thox-whitepapers holds no Weight-Space
Programming file (checked 2026-11-04). The HF upload remains open.

v1.1.1 should be built from the v1.1.0 record's sources (the artifact
ZIP on Zenodo, 3fe59756...) with deltas 1 to 4 ported, plus the L1
measurement once Hugging Face billing is restored.

Open for Tommy: the THOX research-paper standard and arXiv policy both
expect an AI-assistance disclosure; v1.1.0 dropped it on the 09:47
ruling. Any arXiv submission needs that settled first.
