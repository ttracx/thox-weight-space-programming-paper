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

Zenodo: DOI 10.5281/zenodo.23954379 reserved on the draft deposit
2026-11-04; files above uploaded to that deposit and published (record
URL and verification appended below when the publish step confirms).

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
