# Development

Paper pipeline (Template v1.0, THOX Research Paper Process v1.0):
`artifact/wp/build.py` generates `paper.src.html` from
`artifact/exp/results/*.json`; `artifact/wp/render.py` renders the PDF
(WeasyPrint), the single-file HTML and the DOCX; `artifact/wp/validate.py`
independently re-derives the paper's numbers from the evidence files and
sweeps for placeholders and internal paths.

Edition discipline: never edit a shipped edition in place. A change is
a new version (build constants in `wp/build.py`), a new Zenodo version,
and a new entry in `.agents/HANDOFF.md` with fresh SHA-256 hashes.

Field lesson recorded in the paper (Section 6): never sign JSON floats
across languages; the patch manifest wire form carries bit patterns
(f32-byte hex) and decimal strings, not JSON numbers.
