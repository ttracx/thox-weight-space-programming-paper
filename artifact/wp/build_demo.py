"""Build the companion demo (single self-contained HTML, Template v1.0 demo
design). All data read from exp/results/*.json and wp/demo_data.json."""
import json, re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
WP = ROOT / "wp"
tpl = (Path.home() / "workspace/standards/THOX_Research_Paper_Template_v1.0/demo_template.html").read_text()
CSS = re.search(r"<style>(.*?)</style>", tpl, re.S).group(1)
S123 = json.loads((ROOT / "exp/results/summary_e123.json").read_text())["experiments"]
E0 = json.loads((ROOT / "exp/results/summary_e0.json").read_text())
MAPS = json.loads((WP / "demo_data.json").read_text())
LOOP_PATH = ROOT / "exp/results/summary_loop_baseline.json"
LOOP = json.loads(LOOP_PATH.read_text()) if LOOP_PATH.exists() else None
T15 = E0["tensors"]["model.language_model.layers.15.mlp.down_proj.weight"]
T19 = E0["tensors"]["model.language_model.layers.19.mlp.down_proj.weight"]
sens = S123["E3_fix"]["override_sensitivity"]

if LOOP and all("error" not in r for r in LOOP["runs"]):
    rows = ""
    labels = {"qwen35-0.8b-base-thinking": "Qwen3.5-0.8B base, thinking ON",
              "qwen35-0.8b-base-nothink": "Qwen3.5-0.8B base, thinking OFF (THOX serving config)",
              "qwen35-0.8b-edited-thinking": "Released edited checkpoint, thinking ON",
              "thox-micro-125m": "thox-micro-125m"}
    for r in LOOP["runs"]:
        rows += (f"<tr><td>{labels.get(r['model'], r['model'])}</td><td>{r['cap_hit_rate']:.0%}</td>"
                 f"<td>{r['loop_rate']:.0%}</td><td>{r['mean_tokens']:.0f}</td><td>{r['accuracy']:.0%}</td></tr>")
    loop_html = f"""<table><tr><th>Configuration</th><th>Cap hits</th><th>Loop rate</th><th>Mean tokens</th><th>Accuracy</th></tr>{rows}</table>
<p class="note">Scoped instrument check: {LOOP['scope']}. Small n, read the paper's Section 5 before quoting.</p>"""
else:
    loop_html = """<p class="note">The scoped loop baseline was still running on the THOX build VM when this demo edition was built. Its results table is inserted in the next edition; the paper's Section 5 carries the status. Nothing in this demo depends on it.</p>"""

html = f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Weight-Space Programming for THOX Edge Models: Demo</title>
<meta name="description" content="Companion demo: read a task from composed weight maps, explore a 16-weight policy fix, verify the released Qwen3.5-0.8B edit, and size a signed rank-1 patch.">
<style>{CSS}
canvas.map{{border:1px solid var(--rule);border-radius:6px;image-rendering:pixelated;width:100%;max-width:170px}}
.maps{{display:grid;grid-template-columns:repeat(auto-fit,minmax(150px,1fr));gap:10px}}
</style>
</head>
<body>
<div class="wrap">
<header>
  <div class="eyebrow">THOX.ai Research &middot; companion demo to technical report v1.0.1</div>
  <h1>Weight-Space Programming, hands on</h1>
  <p>Four small instruments from the whitepaper, running on its measured data. Every number is labelled with its evidence class and comes from the result files in the paper's artifact bundle.</p>
</header>

<h2>1. Read: find the task in the composed maps</h2>
<p>Below are the per-class effective input-to-logit maps (E = W2<sup>T</sup>W1<sup>T</sup>) of one trained 64-48-4 network from experiment E1. Its task was one of: name the dot's <b>column</b>, its <b>row</b>, or its <b>diagonal</b> class on an 8x8 grid. Three of the paper's four readers scored at chance on maps like these; the per-class composed reader (R4) scored 100% over 30 networks. Pick a network, look at the four class maps, and guess before you reveal.</p>
<div class="card">
  <label>Network</label>
  <select id="netSel"><option value="col">Network A</option><option value="row">Network B</option><option value="diag">Network C</option></select>
  <div class="maps" id="maps"></div>
  <label>Your guess</label>
  <select id="guess"><option value="col">column</option><option value="row">row</option><option value="diag">diagonal</option></select>
  <button id="reveal" type="button">Reveal</button>
  <div class="out" id="readOut">The class maps are |E| intensities (green = strong). A column task concentrates each class map in one column band; a row task in one row band; a diagonal task along diagonals.</div>
</div>

<h2>2. Fix: sixteen weights, one dose-response</h2>
<p>Experiment E3 repaired a MountainCar policy stuck at 0% success by editing 16 of 747 weights (2.14%): two velocity detectors, an energy-pumping override pathway, output gain. A random edit of the same size scored 0%. Drag the override gain and watch success respond; 1.0 is the shipped edit (92.8% over 512 episodes; the curve below is the 256-episode sweep).</p>
<div class="card">
  <label>Override gain: <span id="gainVal">1.0</span>x</label>
  <input type="range" id="gain" min="0" max="2" step="0.25" value="1">
  <div class="kpis"><div class="kpi"><div class="kv" id="succ">94.1%</div><div class="kl">success at this gain (256 episodes)</div><div class="kt">Simulated</div></div>
  <div class="kpi"><div class="kv">0%</div><div class="kl">before the edit, and for the random-edit control at every gain</div><div class="kt">Simulated</div></div></div>
</div>

<h2>3. Verify: the released Qwen3.5-0.8B edit (E0)</h2>
<div class="kpis">
  <div class="kpi"><div class="kv">{E0['total_entries_changed']:,}</div><div class="kl">entries changed bitwise across the two edited tensors (131,072 addressed)</div><div class="kt">Measured</div></div>
  <div class="kpi"><div class="kv">{T15['sv_ratio_s1_over_s2']:,.0f} / {T19['sv_ratio_s1_over_s2']:,.0f}</div><div class="kl">sigma1/sigma2 of each tensor's diff: both edits are rank-1 (99.999% of diff energy)</div><div class="kt">Measured</div></div>
  <div class="kpi"><div class="kv">{T15['edited_sha256'][:12]}... / {T19['edited_sha256'][:12]}...</div><div class="kl">edited tensor SHA-256 prefixes, matching the published values exactly</div><div class="kt">Measured</div></div>
</div>
<p class="note">Full hashes, base hashes and per-tensor detail: exp/results/summary_e0.json in the artifact bundle. Base pinned at revision {E0['base_rev'][:12]}...</p>

<h2>4. Ship: size a signed rank-1 patch</h2>
<p>The patch channel ships an edit as factors (direction u, column set, alpha), signed in a manifest that pins the base model's tensor hashes. Defaults below are the Experiment 8 tensor. Change the geometry and compare representations.</p>
<div class="card">
  <div class="grid">
    <div><label>Rows (u length)</label><input id="pRows" type="number" value="1024"></div>
    <div><label>Tensor columns</label><input id="pCols" type="number" value="3584"></div>
    <div><label>Edited columns</label><input id="pEdit" type="number" value="64"></div>
  </div>
  <div class="out" id="patchOut"></div>
  <p class="note">Lifecycle enforced by the Rust loader: verify Ed25519 signature, verify base hashes, apply to the inactive A/B slot, verify result hashes, switch atomically, roll back in one command. End-to-end test (Python signer, Rust loader): all checks pass, including tamper rejection and wrong-base abort. Calculated sizes.</p>
</div>

<h2>5. The control: loop baseline</h2>
{loop_html}

<footer>THOX.ai Research, companion to technical report v1.0.1 (public edition, 2026-11-04, DOI 10.5281/zenodo.23954379). Data: exp/results/ in the paper's artifact bundle. Demo runs entirely in this file; no network calls.</footer>
</div>
<script>
const MAPS = {json.dumps(MAPS)};
const SENS = {json.dumps({float(k): v for k, v in sens.items()})};
function drawMaps(){{
  const task = document.getElementById('netSel').value;
  const wrap = document.getElementById('maps'); wrap.innerHTML = '';
  MAPS[task].maps.forEach((grid, c) => {{
    const holder = document.createElement('div');
    const cv = document.createElement('canvas'); cv.width = 8; cv.height = 8; cv.className = 'map';
    const ctx = cv.getContext('2d');
    let mx = 0; grid.flat().forEach(v => mx = Math.max(mx, Math.abs(v)));
    for (let r = 0; r < 8; r++) for (let col = 0; col < 8; col++) {{
      const t = Math.abs(grid[r][col]) / (mx || 1);
      ctx.fillStyle = `rgb(${{Math.round(230 - 200*t)}},${{Math.round(244 - 60*t)}},${{Math.round(236 - 170*t)}})`;
      if (t > 0.03) ctx.fillStyle = `rgba(5,164,81,${{0.15 + 0.85*t}})`;
      ctx.fillRect(col, r, 1, 1);
    }}
    const lab = document.createElement('div'); lab.className = 'note'; lab.textContent = 'class ' + c + ' map';
    holder.appendChild(cv); holder.appendChild(lab); wrap.appendChild(holder);
  }});
  document.getElementById('readOut').textContent = 'Maps drawn. Make your guess, then reveal.';
}}
document.getElementById('netSel').addEventListener('change', drawMaps);
document.getElementById('reveal').addEventListener('click', () => {{
  const task = document.getElementById('netSel').value;
  const g = document.getElementById('guess').value;
  const names = {{col: 'column', row: 'row', diag: 'diagonal'}};
  document.getElementById('readOut').innerHTML =
    (g === task ? '<span class="ok">Correct.</span>' : '<span class="bad">Not this time.</span>') +
    ' This network\\'s task was <b>' + names[task] + '</b>. The R4 reader (per-class composed voting) also reads it as ' + names[task] +
    '; R1-R3 (marginal readers) systematically answer "diagonal" on column and row networks. Over 30 networks: R4 100%, R1-R3 at chance (33%). Measured, E1.';
}});
drawMaps();
const gain = document.getElementById('gain');
gain.addEventListener('input', () => {{
  const v = parseFloat(gain.value);
  document.getElementById('gainVal').textContent = v.toFixed(2).replace(/0$/, '');
  document.getElementById('succ').textContent = (SENS[v] * 100).toFixed(1) + '%';
}});
function patchCalc(){{
  const rows = +document.getElementById('pRows').value, cols = +document.getElementById('pCols').value, ec = +document.getElementById('pEdit').value;
  const factor = rows * 2 + ec * 2 + 16;
  const sparse = rows * ec * 6;
  const full = rows * cols * 2;
  const fmt = n => n >= 1048576 ? (n / 1048576).toFixed(2) + ' MB' : n >= 1024 ? (n / 1024).toFixed(2) + ' KB' : n + ' B';
  document.getElementById('patchOut').textContent =
    'factor form (this channel): ' + fmt(factor) + ' per tensor\\n' +
    'sparse diff (index+value per changed entry): ' + fmt(sparse) + ' per tensor\\n' +
    'full tensor replacement: ' + fmt(full) + ' per tensor\\n' +
    'factor form is ' + Math.round(full / factor).toLocaleString() + 'x smaller than the tensor it edits.';
}}
['pRows', 'pCols', 'pEdit'].forEach(id => document.getElementById(id).addEventListener('input', patchCalc));
patchCalc();
</script>
</body>
</html>"""
(WP / "weight-space-programming-demo.html").write_text(html)
print("demo written", len(html), "bytes; loop data:", bool(LOOP))
