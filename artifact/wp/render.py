"""Render paper.src.html -> PDF (WeasyPrint, kvtypeset venv), single-file
HTML (figures inlined), DOCX (LibreOffice). Run with the kvtypeset venv
python for WeasyPrint; DOCX step shells out to soffice."""
import base64, re, subprocess, sys
from pathlib import Path

WP = Path(__file__).resolve().parent
src = (WP / "paper.src.html").read_text()

def inline(html):
    def rep(m):
        path = WP / m.group(1)
        b64 = base64.b64encode(path.read_bytes()).decode()
        return f'src="data:image/png;base64,{b64}"'
    return re.sub(r'src="(figures/[^"]+)"', rep, html)

single = inline(src)
(WP / "paper.html").write_text(single)
print("paper.html (single-file) written", len(single))

try:
    from weasyprint import HTML
    HTML(filename=str(WP / "paper.src.html"), base_url=str(WP)).write_pdf(str(WP / "paper.pdf"))
    print("paper.pdf written")
except ImportError:
    print("WeasyPrint not in this interpreter; run with ~/workspace/kvtypeset venv python")

import shutil, tempfile
tmp = Path(tempfile.mkdtemp()) / "wsp_paper.html"
shutil.copy(WP / "paper.html", tmp)
r = subprocess.run(["soffice", "--headless", "--convert-to", "docx:MS Word 2007 XML",
                    "--outdir", str(tmp.parent), str(tmp)], capture_output=True, text=True, timeout=300)
made = tmp.parent / "wsp_paper.docx"
if made.exists(): shutil.copy(made, WP / "paper.docx")
print("soffice:", r.returncode, r.stdout.strip().splitlines()[-1] if r.stdout else r.stderr[-200:])
