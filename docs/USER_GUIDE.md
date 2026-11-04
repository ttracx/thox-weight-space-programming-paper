# User Guide

## Read the paper
- `paper/Weight-Space-Programming-for-THOX-Edge-Models_v1.0.1.pdf` for print.
- `paper/Weight-Space-Programming-for-THOX-Edge-Models_v1.0.1.html` is a
  single self-contained file (figures inlined); open it in any browser.
- The version of record is the Zenodo deposit, DOI
  10.5281/zenodo.23954379.

## Run the demo
Open `paper/weight-space-programming-demo.html`. It runs entirely
client-side on the paper's measured data: a read-quiz built from real
experiment weights, the E3 edit-gain explorer, E0 verification cards,
and the rank-1 patch-size calculator.

## Verify the headline claim yourself (E0)
`artifact/exp/e0_rebuild.py` downloads the pinned base and edited
tensors and re-checks the counts, hashes and rank-1 structure reported
in Section 4.5. See `docs/QUICKSTART.md`.

## Use the patch channel
`artifact/src/thox-wsp/` contains the toolkit and loader. Its own
README covers the manifest format, signing, apply and rollback. Do not
accept unsigned or unpinned patches: the paper's Section 9 explains why
the signature and base-hash pin are load-bearing.
