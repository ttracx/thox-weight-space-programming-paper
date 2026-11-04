# Weight-Space Programming — Literature Lane

**Paper working title:** THOX Weight-Space Programming whitepaper (in preparation)
**Lane:** Literature / evidence verification
**Date of verification:** 2026-11-03 (America/Chicago)
**Primary source fetched in full:** https://rikiyat.github.io/blog/weight-space-programming/
**Verification method:** Every arXiv citation marked VERIFIED below was opened on its arXiv abstract page in this lane on 2026-11-03 and its authors, title, arXiv ID and first-submission date were copied from that page. Entries that were not opened that way are marked UNVERIFIED or SEARCH-ONLY explicitly. No arXiv ID in this file was invented or reconstructed from memory alone — unverified IDs are flagged, not silently presented as fact.
**Evidence discipline:** This file separates three layers throughout: (A) what the source post *claims*, (B) what a public artifact *independently shows* (HF checkpoint, hash-verified diff, re-run), and (C) secondary commentary. Do not collapse A into B in the whitepaper.

---

## 1. Verified summary of the source post

### 1.0 Bibliographic identity

- **Title:** "Sparks of Weight-Space Programming: LLMs can natively read & write neural network weights"
- **Authors:** Rikiya Takehi, Jayden Teoh, Alex Zhang, Omar Khattab. Takehi and Teoh are described in secondary coverage of the release as co-first authors. All four are listed with MIT CSAIL affiliations in the Kingy AI summary (Section 4); the blog page text fetched in this lane does not itself render a byline block, so affiliation is secondary-sourced, not primary-verified.
- **Venue / form:** Research blog post, **not peer-reviewed, no arXiv paper** as of 2026-11-03. Published **2026-11-02** (page metadata: `Published: 2026-11-02T00:00:00-08:00`).
- **Editor model:** A frontier LLM the authors call "GPT-6 Astra" (also "Astra"). The identity, weights and availability of Astra cannot be independently verified from the public artifacts in this lane; treat "GPT-6 Astra" as the authors' designation.
- **Definition (authors'):** *Weight-Space Programming* = a general-purpose LLM **reads and writes a network's weights directly** — not through an optimizer, and in particular not with gradient descent — around a natural-language specification, sometimes with no environment feedback at all.
- **Public logs:** Complete logs for every experiment are released at `github.com/RikiyaT/lm_understand-logs` (prompts, replies with reasoning summaries, code run, outputs seen, networks read/written, evaluation behind each number), per the post's Logs section. This lane did not audit the full log repository line-by-line; specific log-derived facts below are attributed to the HF card or to Kingy AI's inspection of the logs, not to a lane audit.
- **Local PDF note:** The PDF supplied to THOX (`Sparks_of_Weight-Space_Programming_LLMs_can_natively_read___write_neural_network_weights.pdf`) is truncated after Experiment 6. Sections 1.3–1.4 below come from the **full web version**, fetched 2026-11-03, and are the parts missing from that PDF.

### 1.1 Experiments 1–6 (context, brief — all are source claims)

| Exp | Task | Setup (as stated) | Claimed result |
|---|---|---|---|
| 1 — Read | Name the game a PPO policy was trained on, from weights as text only, no tools, no game options given | MLP 500→32→32→5, tanh, 17,253 weights; grid versions of Breakout, Pong, Pac-Man, Freeway; same architecture for all; PPO 1B steps, best of 3 seeds | Correct game named for **all 4** networks. Authors' gloss: first-layer weight concentration (e.g. Breakout paddle along bottom row) and output-layer distinctions. |
| 2 — Read | Name what a DDPM will generate, weights only, no tools / no forward pass | MLP 160→64→64→144, ReLU, 23,824 weights; 12×12 grayscale circles / squares / triangles; Adam 40k steps | Correct shape for all 3. Astra drew shapes as **outlines** although models generate filled shapes — authors cite this error as evidence it read weight geometry rather than simulating a forward pass. |
| 3 — Read | Name training language + identify every attention head's function, from **middle layers only** (embeddings and unembedding removed, model cannot be run) | Char-level transformers, 4 layers × 6 heads, width 384, 7.16M weights; trained on 1B chars each of Python code, Japanese romaji (Aozora Bunko), English Wikipedia; Python analysis allowed (≤100 runs), running any layer on any input forbidden and, authors state, checked | Correct language for all 3 models in **both attempts**; **every copying (induction) head found, no false positives** (Python: 2.1, 3.1, 3.5; Romaji: 3.3; English: 3.1; ground truth measured by a repeated-string probe, copying heads 0.22–0.55, all others ≤0.02). Authors note Astra's matrix-multiplication method rediscovers the Elhage et al. circuit analysis, which was never mentioned to it. |
| 4 — Fix | Fix a PPO car policy stuck in a local minimum (drives at ramp, never backs up for a run-up), one reply, no tools | Kinetix actor 679→128→5×128→16, 171,664 weights; official PPO 1B steps; 0 successes in 256 episodes | Edit changed **3.5% of weights**, added a small position/speed path that switches off past the obstacle; **1,024 / 1,024 episodes succeed**. |
| 5 — Write from scratch | Write MinAtar policies as text, one reply, no data / loss / gradients / tools / rollouts | 600→32→32→6, tanh; Breakout, Seaquest, Asterix; 1,000 episodes scored | Breakout **517.4** vs PPO-100M 15.8 / PPO-500M 25.3; Seaquest 53.1 vs 5.6 / 88.9; Asterix 53.2 vs 25.8 / 55.2. I.e. beats PPO-100M in all three; beats / nearly matches PPO-500M only in Breakout / Asterix. |
| 6 — Write with tools | Write a 9×9 Go policy from scratch, Python sandbox, forward-pass budget 0–50 (1 pass = ≤128 games vs a practice opponent, or outputs on ≤256 positions); no training, no search, no running the net outside passes | 243→512×6→82, ReLU, 1,480,274 weights, starting from zero; scored over 2,000 games per opponent | 0 passes: beats two **smaller** PPO nets (243→32→32→82) in >50% of games. 50 passes: beats the **equal-sized** PPO net trained on ~20M games (Kingy, from logs: 74.2% / 70.0% / 78.5% vs three seeds over 2,000 games each). Method, per post: hand-writing a Go program layer-by-layer (liberties → group danger → move scoring). |

### 1.2 Experiment 7 in detail — sycophancy detection (READ; the negative-then-qualified result)

This is the experiment most likely to be mis-summarised in secondary coverage. The headline is **failure from weights alone**, success only after the task was relaxed.

**Question:** Which of two language models was trained to be sycophantic, judged from the weights?

**Setup (as stated in the post):**
- Base model: **Gemma 3 270M, instruction-tuned, 18 layers**.
- **Three pairs** of copies, each pair fine-tuned with exactly the same procedure, settings, data and user messages on the same QA dataset. One copy per pair is trained to give the correct answer; the other to be sycophantic — always giving the answer the user suggests.
- Anti-shortcut control: **token embedding (input) and output layers were frozen** during fine-tuning, so both models share identical input/output layers and Astra cannot solve it from input/output distributions.
- Behavioural ground truth (authors'): on facts the model knows and was **not** trained on, the sycophant follows **100%** of wrong user guesses; the honest model follows **1–3%**.
- Astra receives: both models' weights and tokenizer, Python with numpy, and (in the relaxed condition) an **attention tool**: both models are run on up to 16 texts Astra writes itself, and it receives back **only the attention weights** — not the models' outputs. It may not run the models itself. At most 20 runs.
- Asked: which model is the sycophant, and which layers, heads and MLPs carry the difference.

**Result — weights alone (primary condition): FAILED.**
> "Unfortunately, from the weights alone, Astra was unable to tell. In all four attempts, it identified many differences between the two models in weight space, but was unable to map these into behavioral differences."

**Result — weights + attention patterns (relaxed condition): SUCCEEDED, small n.**
Given attention patterns, Astra **picked out the sycophant in all three pairs** (3/3). Kingy's inspection of the released logs adds: four rounds of weight-only inspection produced no reliable discrimination; with attention patterns it was 3 correct out of 3, with **one final confidence only 55%** — i.e. one of the three successes was near-chance in stated confidence. That confidence detail is log-derived via Kingy, not stated in the blog text.

**Mechanistic gloss (authors'):** In the sycophantic networks, middle-layer attention heads allocate more weight to tokens in the user's suggestion. Worked example in the post (Figure 2), head **10.2** attending from the answer position: honest model attends 94.3% to "the question's numbers" and 0.75% to "the user's answer"; sycophant attends 3.5% to the question's numbers and **85.7%** to the user's answer.

**Correct THOX reading of Exp 7:** Weight-space *reading* of a subtle behavioural trait in a real (270M) LM is **not demonstrated from weights alone**. What is demonstrated is weights-plus-activation-pattern auditing on deliberately trained toy variants, n=3 pairs. This bounds any THOX claim about weight-only backdoor / trait auditing: the source itself is a counterexample at this scale and trait subtlety. The authors' own "What Comes Next" framing of "auditing without evaluation" is presented as a future possibility, not as an Exp 7 result.

### 1.3 Experiment 8 in detail — Qwen3.5-0.8B math fix (WRITE / FIX; the headline result)

**Task (as stated):** Make Qwen3.5-0.8B better at math by editing its weights directly. No gradient descent, no training.

**Setup (as stated):**
- Model: **Qwen3.5-0.8B, thinking on, 24 layers, ~0.8B weights**.
- Harness: Python session (notebook-like, no GPU for the editor) with the model's weights loaded — the same pattern as Experiment 6.
- Practice data: prompts selectable from the **training** sets of GSM8K (**7,469** problems) and MATH (**7,275** problems). Test sets were not given to Astra.
- Feedback budget: **10, 25 or 50 forward passes**. One forward pass = the model answers up to **512 problems**, or reads up to **1,024 texts** (teacher-forced read of internal information). A "pass" is therefore a large batch, not a single example — a point Kingy stresses and the whitepaper must state alongside any "50 passes" phrasing.
- Evaluation (Astra never sees it): MATH-500, GSM8K and six other benchmarks; thinking on; up to **32,768 tokens**. Sampling: **temperature 0.6, top-p 0.95, top-k 20, presence penalty 1.5**. Samples per problem: 4 on MATH-500 / Minerva Math / OlympiadBench / GPQA Diamond, 2 on GSM8K and IFEval, 16 on AMC23, 1 on a fixed 1,000-question MMLU-Pro subset.
- Contamination precaution (log-derived, via Kingy): practice builder filtered normalised exact matches and shared 13-word windows against the math evaluation sets. Useful, but not proof against semantic near-duplicates or pretraining exposure.

**What was diagnosed in the weights (authors' account):**
1. Symptom first: the base model **loops** — it repeats the same text and rarely reaches an answer. **85 of its first 96 practice answers ran to the 32,768-token limit.** Across full MATH-500, **93.0%** of base answers hit the token limit. The post notes Qwen's own model card warns this model is prone to thinking loops, under the sampling used.
2. Localisation: Astra traced the looping to **one direction written by the MLPs of layers 15 and 19** (a "repetition direction" in the residual stream, in the language of the released submission as summarised by Kingy).
3. Intervention: **subtract that direction from 64 output columns of `down_proj` in each of the two layers** — described in the post as "much like removing a behavior by deleting a single direction from a model's weights." Formula from the run's final submission (via Kingy / GitHub logs, not printed in the blog text): `W_new = W_original − 6 × outer(u, mask64 × (u @ W_original))`, where `u` is the estimated unit repetition direction for that layer and the factor 6 means this was a *scaled* subtraction, not a pure projection removal.

**What fraction was edited:**
- **131,072 weights** = 2 layers × 64 columns × 1,024 entries.
- **131,072 / ~0.8B = 0.016%** of the model. Exactly two tensors differ from base (see §1.5 for hashes).
- Kingy, from the released edit manifest: **130,188 entries are bitwise different** after bfloat16 conversion (some computed changes rounded back to the original value); relative change across the two edited matrices ≈ **10.6% and 8.1%**. A small *count* of changed entries does not by itself mean a small *effect* — Kingy makes this point and the whitepaper should keep it.

**Results (authors' evaluation, same sampling for base and edited):**

| Qwen3.5-0.8B | MATH-500 (%) | GSM8K (%) | IFEval (%) | Hit 32k token limit (%) |
|---|---:|---:|---:|---:|
| Base | 7.9 | 13.8 | 21.0 | 93.0 |
| Edited, 10 forward passes | 12.3 | 25.7 | 49.0 | 87.2 |
| Edited, 25 forward passes | 14.1 | 25.1 | 39.9 | 86.4 |
| **Edited, 50 forward passes** | **48.1** | **67.1** | **62.3** | **33.1** |

- **MATH-500 7.9% → 48.1%** = +40.2 points, ≈6.1×. **GSM8K 13.8% → 67.1%** = +53.3 points. Note the dose-response is **nonlinear / threshold-like**: 10 and 25 passes barely move the loop rate (87.2% / 86.4% hitting the limit) and only reach 12–14% on MATH-500; the jump happens at 50 passes, when the loop rate collapses to 33.1%. Do not present this as smooth scaling.
- **IFEval effect: 21.0% → 62.3%** = +41.3 points, ≈3.0×. IFEval here is strict prompt-level accuracy (every verifiable constraint in a prompt must pass; Kingy, citing the IFEval protocol and the project's evaluation code). The post's own explanation is the correct one: *"The loops are not special to math, so performance beyond math improved as well."* Kingy's mechanism analysis sharpens it: the evaluation extracts the answer after the thinking section closes; if thinking never closes, the answer is empty and scores zero. A model that **finishes** more often therefore gains IFEval points without necessarily acquiring new instruction-following skill. Paired practice-item analysis (authors', via Kingy): across 1,152 paired GSM8K/MATH practice items, base correct on 122, edited correct on 696; **579 rescued, 5 regressions; 576 of the rescues had originally been truncated**. That is the strongest internal evidence that the dominant mechanism is **recovery of already-present ability by removing a truncation failure**, not teaching new mathematics.
- **What did not become strong:** Released additional evaluations (via Kingy from the logs) include gains on AMC23, Minerva Math, OlympiadBench, a 1,000-question MMLU-Pro subset and GPQA Diamond, but **AIME remained weak after editing: 0.625% on AIME 2024 and 2.292% on AIME 2025**. One-third of edited MATH-500 responses still hit the token cap, and the final run state records whitespace-tail degeneration in 51 of 1,152 edited practice outputs.
- **Cost is not established:** Log-derived (via Kingy): the successful run used GPT-6 Astra through Codex CLI at `max` reasoning effort, 50 harness passes, 80 Python executions, **158 agent turns across four conversations, 20.3 hours elapsed** including 4.7 hours waiting for an unavailable model. The release does **not** establish that this is cheaper than fine-tuning, a sampling change, or another loop-control method. The whitepaper must not claim a cost advantage.

**Additional experiment — Gemma 3 270M, the negative control the headline needs:**
Same editor, a model that does **not** loop (only **8.5%** of answers reach its token limit, vs 93% for Qwen; sampled at its card settings: temperature 1.0, top-k 64, top-p 0.95, up to 8,192 tokens; MATH-500, 4 samples/problem):

| Gemma 3 270M IT | MATH-500 (%) |
|---|---:|
| Base | 6.8 |
| Edited, 5 passes | 7.0 |
| Edited, 10 passes | 7.6 |
| Edited, 25 passes | 7.7 |
| Edited, 50 passes | 7.0 |

Authors' conclusion, quoted in substance: Astra found ordinary reasoning errors (wrong arithmetic, invalid algebra) with **no single component behind them to switch off**; its edits stayed small and targeted (e.g. doubling one number-responsive neuron) and none moved MATH-500 by more than about a point, a gain Astra itself reported as not established. *"Editing weights could remove an obstacle that hid an ability, but it could not add an ability the model lacked."* This sentence is the single most important scope limiter in the post for THOX purposes.

### 1.4 Limitations and caveats

**Stated by the authors:**
1. "Very early results"; capabilities "are exciting but still limited, specifically due to inefficiencies in context length and harnesses."
2. The Gemma negative result above: the method removes obstacles, it does not add missing capability (authors' own framing).
3. Exp 7 weights-only failure (stated plainly in the post).
4. A benchmark and harness for Weight-Space Programming are still **being built** — i.e. no standardised evaluation exists yet, by the authors' own account.

**Established by the public artifacts / careful secondary inspection (Kingy, HF card) — attribute, do not present as lane-run experiments:**
5. **Broken-baseline flattery:** The base score of 7.9% is obtained under sampling (temperature 0.6) at which this specific model is known — per its own model card, as noted in the post — to loop on 93% of problems. Qwen's card lists different recommended thinking-mode sampling (Kingy: including temperature 1.0) and its reported benchmark scores use different conditions and are not directly comparable. The missing control is base-vs-edited under **matched recommended sampling plus simple non-weight loop controls** (repetition penalties, sampling changes, loop detectors). Until that control exists, "6×" measures recovery from a pathological decoding regime as much as it measures weight-editing power.
6. **"No feedback" does not describe Exp 8.** Exps 1, 2 and 5 are genuinely zero-feedback. Exp 8 used practice problems, inference outputs, internal-state reads and 50 large-batch passes; Exp 6 used up to 50 passes; Exp 7's success condition used attention patterns from model runs. Any THOX sentence of the form "with no feedback, Astra fixed Qwen" is false.
7. **"No gradients" ≠ "no data, no compute, no optimisation."** The target model was not gradient-trained, but the editor is itself a trained frontier model running 158 turns of hypothesis-test-revise search, guided by a human-designed task that (per the released instructions, via Kingy) advised diagnosing failures, testing causal interventions and confirming gains on held-out practice items, and specified protected parts of the model.
8. **Scale demonstrated is small.** Reading-from-text tops out at 171,664 weights (Exp 4). Tool-assisted writing tops out at 1.48M weights from scratch (Exp 6) and editing at 0.8B (Exp 8) — where the edit itself touched only two matrices. Nothing in the post demonstrates reading, writing or editing at frontier scale (tens/hundreds of billions), or cross-architecture circuit grafting; both appear only in the "What Comes Next" speculation list, alongside recursive self-improvement and zero-data steering/unlearning. Keep those in the future-work tense.
9. **Replication status:** One independent re-run of the *edited checkpoint* exists (§1.5, 51.0% on MATH-500) — it verifies that the released weights score as claimed, under the post's protocol. It does **not** replicate the *editing process* (that Astra, given the base model, finds this edit), nor GSM8K / IFEval. A separate reported replication (Alex Krentsel, via Kingy / X, 2026-11-02) covers only Exp 5-style Breakout writing across model generations. Selection effects cannot be fully assessed: Kingy notes the release discloses that earlier prompt trials are not included, the editing harness and some grader modules are absent, and evaluation scripts retain internal paths.
10. **Peer review:** None. Blog post + public logs + rebuilt checkpoint is a strong transparency package for a blog post, and a weaker evidence class than a peer-reviewed paper or an independent process replication. The THOX paper must label it MEASURED-BY-AUTHORS / ARTIFACT-VERIFIED (for the checkpoint score) accordingly, per THOX evidence-class discipline.

### 1.5 Hugging Face artifacts — what was checked

Two model repos carry the same edited checkpoint. This lane opened both cards and both file trees on 2026-11-03.

**(a) `RikiyaT/Qwen3.5-0.8B-weight-space-programming`** — the author-namespace release linked from the post.
**(b) `ML-Intern-lab/Qwen3.5-0.8B-weight-space-programming`** — the ML Intern rebuild (authored by akhaliq / HF staff; commit messages credit ML Intern). Its card states, in a line the whitepaper should quote rather than paraphrase away: this is *"the model from 'Sparks of Weight Space Programming' (Experiment 8) — the one the blog post did not release"* — i.e. the original post evaluated a text-only export and did not itself ship this checkpoint; Ahsen Khaliq rebuilt it from the logs with ML Intern on HF Jobs, 2026-11-02, and the post thanks him for rebuilding it, re-running its evaluation and making the live demo.

**Card claims (both cards, consistent):**
- Edit: 131,072 weights, 64 MLP output columns in each of layers 15 and 19, `down_proj`; no gradient descent / training / fine-tuning.
- Astra's edit is published as a **bit-exact diff** in `RikiyaT/lm_understand-logs` (`exp8_math/runs/p50c/edit/`). The checkpoint was rebuilt with the authors' `exp8_math/code/apply_edit.py`, which **sha256-verifies every rebuilt tensor against the checkpoint evaluated in the post**.
- Only two tensors differ from base `Qwen/Qwen3.5-0.8B` @ `2fc06364715b967f1860aea9cf38778875588b17`:
  - `model.language_model.layers.15.mlp.down_proj.weight` — sha256 of raw bfloat16 bytes: `82e2d733ea64feaeb4af93a1e065641d3df98b494a8b7576ef2f52e90fe2ee53`
  - `model.language_model.layers.19.mlp.down_proj.weight` — sha256: `8ef3c61bc36af113ad58e89dbb0a4a14dcba5a45cb750c15ab515c82ddd12eb2`
- One deliberate substitution vs the original evaluation: the post evaluated a **text-only export**; these checkpoints are the **full multimodal release**. Cards assert the language-model tensors are identical (hash-verified) and text prompts do not use the vision tower.
- Base model licence: Apache-2.0 (Qwen/Qwen3.5-0.8B). Logs repo licence: CC BY 4.0 / MIT (per RikiyaT card provenance section).
- Usage snippet uses vLLM, `dtype="bfloat16"`, `max_model_len=34816`, thinking on, and the post's sampling (temperature 0.6, top_p 0.95, top_k 20, presence_penalty 1.5, max_tokens 32768).

**Independent re-run (reported on both cards; performed by akhaliq with ML Intern, NOT by this lane and NOT by the original authors):**
- Full MATH-500: **500 problems × 4 samples = 2,000 generations, 43.4M generated tokens, 51 min on an NVIDIA H200**, vLLM 0.33.0 / transformers 5.20.2 / math-verify 0.9.0, post's protocol, seed 0, last `\boxed{}` graded.
- Edited model: **51.0%** (vs post's 48.1%), **31.6%** hitting the token limit (vs post's 33.1%). Kingy independently recounted the stored correctness flags: 1,020 successes / 2,000 generations — verifying the arithmetic in the artifact, not the execution.
- Base comparison in the re-run is **only a 25-problem smoke test: 5.0%, 95% hitting the limit** — not a matched full-benchmark base run. There is **no independent GSM8K or IFEval replication** in the release.
- Raw scores, per-problem results and sample generations are in each repo's `eval/` folder (claimed on card; this lane confirmed the `eval/` folder exists in both file trees, and did not re-grade its contents).

**Files (identical structure in both repos; sizes from the RikiyaT tree, ML-Intern-lab tree matches except README):**

| File | Size |
|---|---|
| `model.safetensors-00001-of-00001.safetensors` (single shard, Xet) | 1.75 GB |
| `model.safetensors.index.json` | 50.9 kB |
| `tokenizer.json` | 12.8 MB |
| `vocab.json` | 6.72 MB |
| `merges.txt` | 3.35 MB |
| `chat_template.jinja` | 7.76 kB |
| `tokenizer_config.json` | 16.7 kB |
| `config.json` | 2.91 kB |
| `README.md` | 4.88 kB (RikiyaT) / 4.35 kB (ML-Intern-lab) |
| `LICENSE` | 11.5 kB |
| `.gitattributes` | 1.57 kB |
| `preprocessor_config.json` / `video_preprocessor_config.json` | 390 B / 385 B |
| `eval/` | folder (re-run artifacts) |

**Demo Space:** Both cards link **"Try it live"** to `akhaliq/weight-space-programming-demo` (HF Space; its HF page title renders as "Weight-Space-Programmed Qwen3.5-0.8B — a Hugging Face Space by ML-Intern-lab", which is the source of the "ML-Intern-lab demo Space" naming). Card description: *"type a problem, watch the base model loop while the edited one solves it."* **Lane limitation, stated honestly:** the text fetch of the Space returned only its metadata shell ("Fetching metadata from the HF Docker repository…"); this lane did **not** run the demo, did not inspect its runtime files, and cannot verify from this fetch which checkpoint(s) it serves, its hardware, or whether it was live at check time. A live-browser check is required before the THOX paper links it as a working demo.

---

## 2. Rolling literature corpus

Scope: foundations named in the brief, plus the Nov 2025 – Nov 2026 window where genuinely relevant work exists. Organised by the question each strand answers for Weight-Space Programming. "First public" = arXiv v1 submission date as shown on the abstract page opened in this lane, unless noted.

### 2.1 Weight-space learning & weight-space classifiers (reading weights with a *trained* reader)

| # | Authors | Title | Venue / ID | First public | One-line relevance | Status |
|---|---|---|---|---|---|---|
| W1 | Gabriel Eilertsen, Daniel Jönsson, Timo Ropinski, Jonas Unger, Anders Ynnerman | Classifying the classifier: dissecting the weight space of neural networks | arXiv:2002.05688; ECAI 2020 | 2020-02-13 | Trained deep meta-classifiers read training-setup properties directly from weights (16K nets, 320K snapshots) — the trained-reader ancestor of Exp 1–3. | VERIFIED (arXiv page opened) |
| W2 | Thomas Unterthiner, Daniel Keysers, Sylvain Gelly, Olivier Bousquet, Ilya Tolstikhin | Predicting Neural Network Accuracy from Weights | arXiv:2002.11448 | 2020-02-26 | Accuracy predictable from weights alone (R² > 0.98 ranking, simple weight statistics) — weights legibly encode behaviour/performance. | VERIFIED |
| W3 | William Peebles, Ilija Radosavovic, Tim Brooks, Alexei A. Efros, Jitendra Malik | Learning to Learn with Generative Models of Neural Network Checkpoints (G.pt) | arXiv:2209.12892 | 2022-09-26 | A diffusion transformer *trained on checkpoints* generates parameter updates conditioned on a prompted loss — trained weight-writer, contrast class to an untrained LLM editor. | VERIFIED |
| W4 | Xiaolong Han, Zehong Wang, Bo Zhao, Binchi Zhang, Jundong Li, Damian Borth, Rose Yu, Haggai Maron, Yanfang Ye, Lu Yin, Ferrante Neri | A Survey of Weight Space Learning: Understanding, Representation, and Generation | arXiv:2603.10090 | 2026-03-10 | First unified WSL taxonomy (Understanding / Representation / Generation) — the field-framing citation for the THOX paper's related-work section; post-dates the Nov 2025 window opening and pre-dates the source post. | VERIFIED |
| W5 | Prakhar Kaushik, Shravan Chaudhari, Ankit Vaidya, Rama Chellappa, Alan Yuille | The Universal Weight Subspace Hypothesis | arXiv:2512.05117 (v3 revised 2026-10-05) | 2025-12-04 | Spectral analysis of 1,200+ models (500 Mistral-7B LoRAs, 500 ViTs, 50 LLaMA-8B) finds shared low-dimensional weight subspaces across tasks — a candidate *reason* sparse/directional edits and LoRA work at all; in-window (Dec 2025). Note: secondary stress-test coverage disputes how much task-specific signal the ~16 directions carry vs a shared group-mean direction — cite the hypothesis as contested, not settled. | VERIFIED (arXiv page opened); interpretation contested in secondary coverage seen in this lane |

### 2.2 Hypernetworks & trained weight generation (writing weights with a *trained* writer)

| # | Authors | Title | Venue / ID | First public | One-line relevance | Status |
|---|---|---|---|---|---|---|
| H1 | David Ha, Andrew Dai, Quoc V. Le | HyperNetworks | arXiv:1609.09106; ICLR 2017 | 2016-09-27 | One network generates another's weights, trained end-to-end — the foundational "weights as output" move; fast-weight-programmer lineage goes back to Schmidhuber (1992), cited within. | VERIFIED |
| H2 | Rujikorn Charakorn, Edoardo Cetin, Yujin Tang, Robert Tjarko Lange | Text-to-LoRA: Instant Transformer Adaption | arXiv:2506.06105; ICML 2025 | 2025-06-06 | A hypernetwork trained on 9 LoRA adapters writes a new LoRA from a natural-language task description in one forward pass, with zero-shot generalisation to unseen tasks — the closest trained analogue to "just ask for weights in natural language," and the key contrast: T2L's writer is *trained for the job*, Astra is not. | VERIFIED |
| H3 | M. H. I. Abdalla, Zhipin Wang, Christian Frey, Steffen Eger, Josif Grabocka | Zhyper: Factorized Hypernetworks for Conditioned LLM Fine-Tuning | arXiv:2510.19733 | 2025-10-22 | Factorised hypernetwork generates context-aware LoRA adapters from text with up to 26× fewer parameters — in-window evidence the trained-hypernetwork route is still actively improving months before the source post. | VERIFIED |

### 2.3 Model editing (algorithmic, locate-then-edit — writing weights with a *fixed algorithm*)

| # | Authors | Title | Venue / ID | First public | One-line relevance | Status |
|---|---|---|---|---|---|---|
| E1 | Kevin Meng, David Bau, Alex Andonian, Yonatan Belinkov | Locating and Editing Factual Associations in GPT (ROME) | arXiv:2202.05262; NeurIPS 2022 | 2022-02-10 | Causal tracing locates factual recall in mid-layer MLPs; a rank-one update to one MLP rewrites a fact — the direct procedural ancestor of Exp 8's "find the MLP direction, edit `down_proj`" shape, differing in that ROME's edit is computed by a closed-form algorithm, not reasoned out by an LLM. | VERIFIED |
| E2 | Kevin Meng, Arnab Sen Sharma, Alex Andonian, Yonatan Belinkov, David Bau | Mass-Editing Memory in a Transformer (MEMIT) | arXiv:2210.07229; ICLR 2023 | 2022-10-13 | Scales locate-then-edit to thousands of associations across a range of MLP layers (GPT-J 6B, GPT-NeoX 20B) — the scale reference for algorithmic editing vs Exp 8's single-behaviour edit at 0.8B. | VERIFIED |
| E3 | Andy Zou et al. (22 authors) | Representation Engineering: A Top-Down Approach to AI Transparency (RepE) | arXiv:2310.01405 | 2023-10-02 | Concepts as linear directions in residual-stream representation space, read and controlled by direction arithmetic — the conceptual bridge between activation steering and Exp 8's *permanent* version: subtracting a direction from weights instead of adding a vector to activations at inference. | VERIFIED |

### 2.4 Weight arithmetic: LoRA, task vectors, soups and merging (writing weights by *algebra on trained deltas*)

| # | Authors | Title | Venue / ID | First public | One-line relevance | Status |
|---|---|---|---|---|---|---|
| A1 | Edward J. Hu, Yelong Shen, Phillip Wallis, Zeyuan Allen-Zhu, Yuanzhi Li, Shean Wang, Lu Wang, Weizhu Chen | LoRA: Low-Rank Adaptation of Large Language Models | arXiv:2106.09685; ICLR 2022 | 2021-06-17 | Adaptation as a small low-rank weight delta, freezable/mergable back into base weights — defines the delta-object that merging, T2L and most practical weight arithmetic operate on. | VERIFIED |
| A2 | Mitchell Wortsman et al. (11 authors) | Model soups: averaging weights of multiple fine-tuned models improves accuracy without increasing inference time | arXiv:2203.05482; ICML 2022 | 2022-03-10 | Plain weight averaging of fine-tunes from a shared basin beats the best single model — the simplest proof that weight space is algebraically well-behaved. | VERIFIED |
| A3 | Gabriel Ilharco, Marco Tulio Ribeiro, Mitchell Wortsman, Suchin Gururangan, Ludwig Schmidt, Hannaneh Hajishirzi, Ali Farhadi | Editing Models with Task Arithmetic | arXiv:2212.04089; ICLR 2023 | 2022-12-08 | Task vectors (fine-tuned minus pre-trained weights) can be added, negated and combined by analogy to steer behaviour — the canonical "weight arithmetic" citation; Exp 8's direction subtraction is a member of this family, discovered by reasoning rather than by fine-tuning a donor. | VERIFIED |
| A4 | Prateek Yadav, Derek Tam, Leshem Choshen, Colin Raffel, Mohit Bansal | TIES-Merging: Resolving Interference When Merging Models | arXiv:2306.01708; NeurIPS 2023 | 2023-06-02 | Trim / elect-sign / disjoint-merge resolves sign and redundancy interference between task vectors — merging is not naive averaging once donors disagree. | VERIFIED |
| A5 | Le Yu, Bowen Yu, Haiyang Yu, Fei Huang, Yongbin Li | Language Models are Super Mario: Absorbing Abilities from Homologous Models as a Free Lunch (DARE) | arXiv:2311.03099; ICML 2024 | 2023-11-06 | Randomly dropping 90–99% of delta parameters and rescaling preserves SFT ability — direct evidence most fine-tuning deltas are redundant, which is *why* a 0.016% edit can be behaviourally large. | VERIFIED |

### 2.5 Mechanistic interpretability of attention heads (reading circuits from weights)

| # | Authors | Title | Venue / ID | First public | One-line relevance | Status |
|---|---|---|---|---|---|---|
| M1 | Nelson Elhage, Neel Nanda, Catherine Olsson et al. | A Mathematical Framework for Transformer Circuits | Transformer Circuits Thread (transformer-circuits.pub), **no arXiv ID** | 2021-12-22 | QK/OV circuit decomposition, residual-stream-as-communication-channel, "virtual weights" from multiplying matrices across layers, and the first induction-head account — the exact method the post says Astra independently reinvented in Exp 3. | VERIFIED (publisher page opened; date/authorship corroborated in search results — it is not an arXiv paper and must not be given an arXiv ID) |
| M2 | Catherine Olsson, Nelson Elhage, Neel Nanda et al. (26 authors) | In-context Learning and Induction Heads | arXiv:2209.11895 | 2022-09-24 | Induction heads ([A][B]…[A]→[B]) as the mechanism of most in-context learning, developing at the loss "bump" — defines the "copying heads" Astra had to find from weights alone in Exp 3. | VERIFIED |
| M3 | David Lindner, János Kramár, Sebastian Farquhar, Matthew Rahtz, Thomas McGrath, Vladimir Mikulik | Tracr: Compiled Transformers as a Laboratory for Interpretability | arXiv:2301.05062 | 2023-01-12 | Compiles human-readable programs (RASP) *into* transformer weights with known ground-truth structure — proof-by-construction that programs can be hand-written into weights, the deliberate-design precedent for Exps 5–6, and a ground-truth testbed for weight-reading claims. | VERIFIED |

### 2.6 LLM-as-optimizer (the paradigm Exp 8 extends from text artifacts to weights)

| # | Authors | Title | Venue / ID | First public | One-line relevance | Status |
|---|---|---|---|---|---|---|
| O1 | Chengrun Yang, Xuezhi Wang, Yifeng Lu, Hanxiao Liu, Quoc V. Le, Denny Zhou, Xinyun Chen | Large Language Models as Optimizers (OPRO) | arXiv:2309.03409; ICLR 2024 | 2023-09-07 | An LLM iteratively proposes solutions from a natural-language task description plus scored history (prompts, small numeric problems) — the "reasoning-driven optimisation" lineage the post explicitly extends, for the first time in the source work, to *differentiable weights themselves*. | VERIFIED |

### 2.7 Explicitly unverified / not included

- No citation in §§2.1–2.6 is marked UNVERIFIED: every entry above was opened in this lane. That is a deliberate scope choice — several plausible additions were **excluded rather than listed unverified**, including: Deep Weight Space Networks / Graph Metanetworks (Navon / Lim et al.), hyper-representations (Schürholt et al.), Neural Functionals (Zhou et al.), Contrastive Activation Addition (Rimsky et al., arXiv:2312.06681 — seen only in other papers' reference lists in this lane), SALVE (seen only as an alphaXiv PDF in search results), and DeepWeightFlow (seen only as an ICLR 2026 proceedings PDF in search results). If the whitepaper needs any of these, verify the abstract page first and upgrade this section; **do not cite them from this file.**
- The source post's own Background section gestures at further categories (LLMs running/improving training, gradient-free trial-and-error weight search, AdderBoard-style hand-set tiny-transformer weights, models trained to read activations/weights, neuron explainers, weight-reading benchmarks) without the fetched text exposing its underlying reference list. Those pointers are noted here as **source-asserted, lane-unverified**.

---

## 3. Research comparison matrix

Columns per brief: **Reads weights / Writes weights / Uses gradients** (in the weight-producing step itself; a method whose *donor models* were gradient-trained but whose edit step is gradient-free is marked No* with the note) / **Scale demonstrated** / **Feedback needed** (environment / evaluation feedback in the loop).

| Approach (exemplar) | Reads weights? | Writes weights? | Uses gradients? | Scale demonstrated | Feedback needed |
|---|---|---|---|---|---|
| **Weight-Space Programming, zero-shot reading** (Takehi et al. Exps 1–2) | Yes — raw weights as text, no tools | No | No | 17k–24k weights | **None** |
| **WSP, middle-layer reading** (Exp 3) | Yes — transformer blocks only, via Python statistics / matrix products | No | No | 7.16M weights | None (forward passes forbidden) |
| **WSP, sycophancy audit** (Exp 7) | Yes — plus attention patterns in the successful condition | No | No | 270M LM, 3 pairs | Attention patterns from ≤16 self-written texts; **weights-only condition failed** |
| **WSP, one-shot repair** (Exp 4) | Yes — weights as text + 1 recorded episode | Yes — 3.5% edited, single reply | No | 172k weights | One recorded failure episode; no iterative feedback |
| **WSP, from-scratch writing** (Exp 5) | No (weights start at zero / are authored) | Yes — weights emitted as text | No | ~20k weights | **None** |
| **WSP, tool-assisted writing** (Exp 6, Go) | Yes — own tensors in sandbox | Yes — via Python code | No (search also forbidden) | 1.48M weights | 0–50 batched forward passes; quality scales with budget |
| **WSP, LM editing** (Exp 8) | Yes — weights + activations via Python kernel | Yes — 0.016% (2 tensors) | No | **0.8B LM edited**; negative control at 270M | 10–50 large-batch forward passes on practice problems (see §1.3) |
| **Trained weight classifiers** (Eilertsen W1; Unterthiner W2) | Yes — a *separate trained* meta-model consumes weights | No | Yes — to train the reader (not at read time) | Small CNN zoos (16K–120K nets) | Training zoo + labels for the reader; none at inference |
| **Trained weight generation** (G.pt W3; HyperNetworks H1) | Yes — generator conditions on checkpoint weights | Yes — generates / updates weights | Yes — generator is gradient-trained on checkpoint corpora | Small nets (MLP / CNN / RL policies) | Prompted target metric (G.pt); task data during generator training |
| **Text-conditioned hypernetworks** (Text-to-LoRA H2; Zhyper H3) | Partial — conditions on text (+ donor adapters in training), not on target weights | Yes — writes a LoRA adapter | Yes — hypernetwork is gradient-trained once | LLM-scale targets, adapter-size outputs | None at use time; donor adapters + training upfront |
| **Locate-then-edit** (ROME E1; MEMIT E2) | Partial — causal tracing reads *activations* to locate, then reads the target MLP weights | Yes — closed-form rank-one / multi-layer updates | No* — edit is closed-form; locating uses forward/backward interventions, not training | GPT-2 XL → GPT-NeoX 20B; thousands of facts (MEMIT) | A fact / association specification + evaluation prompts per edit |
| **Direction / representation methods** (RepE E3; steering vectors) | Yes — reads activations to extract a direction | Usually **No** — vector added to activations at inference; permanent weight-folded variants exist | No | LLaMA-2 up to 70B (RepE reading/control demos) | Contrastive example pairs to extract the direction |
| **Weight arithmetic on trained deltas** (LoRA A1; Soups A2; Task Arithmetic A3; TIES A4; DARE A5) | Yes — reads donor / base checkpoints to compute deltas | Yes — merged / edited checkpoint is the output | No* in the arithmetic step; **Yes** to produce the donor fine-tunes being combined | Up to ViT-G / 7B-class LLM merges in the cited works | Validation data to select donors / coefficients; no per-edit search |
| **Compiled weights** (Tracr M3) | No (ground truth known by construction) | Yes — a compiler emits weights implementing a specified program | No | Small decoder-only transformers (toy programs) | None — correctness by construction / test programs |
| **Mechanistic circuit analysis** (Elhage M1; Olsson M2) | Yes — weights *and* activations, human analyst + tools | No (analysis only; ablations are diagnostic, not shipped edits) | No | Attention-only toys causally; large LMs correlationally (M2) | Behavioural probes / loss curves to validate circuit hypotheses |
| **LLM-as-optimizer over text artifacts** (OPRO O1) | No — reads scored *candidate solutions*, not weights | No — writes prompts / candidate values, not weights | No | Prompt optimisation at GSM8K / BBH scale | **Iterative** scored feedback every step — the feedback dependence WSP Exp 8 partially inherits and Exps 1/2/5 escape |

**Matrix takeaways for the THOX paper:**
1. The genuinely new cell is not "writes weights without gradients" (ROME, task arithmetic, Tracr and soups all do versions of that) — it is **one untrained, general-purpose reasoner occupying the read + diagnose + write loop across all rows**, including the zero-feedback rows.
2. Feedback is the honest axis: the source's most surprising results (Exps 1, 2, 5) are the zero-feedback ones at small scale; its most useful result (Exp 8) is also its most feedback- and compute-intensive.
3. Every prior writing method either trains its writer (hypernetworks, G.pt), computes its edit by a fixed formula (ROME/MEMIT, merging), or compiles a formal program (Tracr). WSP's writer is none of the three — which is both the claim and the reproducibility risk (§1.4.9).

---

## 4. Kingy AI blog — secondary commentary (NOT primary evidence)

**Item:** "Weight-Space Programming: GPT-6 Astra Edits Qwen", Kingy AI (kingy.ai/blog/weight-space-programming-ai-agent-model-weights), reporting dated 2026-11-02, page updated 2026-11-03. **Status in this paper's evidence hierarchy: secondary commentary.** Kingy inspected the released GitHub logs, edit manifests, evaluation files and HF artifacts and recalculated figures, but states plainly that it **has not replayed the model or the intervention experiments** and has not run the rebuild command it documents. Use it for cross-checks, framing and log-derived detail (each such use is attributed in §1 above); never as the sole citation for a result — cite the post, the logs, or the HF card instead.

**What Kingy adds beyond the post:**
- Full author list with MIT CSAIL affiliations; precise edit arithmetic (2 × 64 × 1,024 = 131,072; ≈0.016% of the nominal 800M) and the manifest correction to **130,188 bitwise-different** entries, with ≈10.6% / 8.1% relative change in the two edited matrices.
- The edit formula `W_new = W_original − 6 × outer(u, mask64 × (u @ W_original))` from the run's final submission, and the run's operational scale: Codex CLI at `max` reasoning, 50 passes / 80 Python executions / 158 turns / four conversations / 20.3 h elapsed (4.7 h waiting). It defines a "pass" honestly (up to 512 generated responses, or 1,024 teacher-forced texts; a paired comparison up to 256 examples per model).
- Practice-item rescue analysis (579 rescued / 5 regressions / 576 rescues originally truncated), the weak AIME results, whitespace-tail degeneration (51/1,152), and the sampling-control critique (§1.4.5) including Qwen-card recommended sampling.
- Independent recount of the HF re-run's stored flags (1,020 / 2,000 = 51.0%), explicitly bounded as verifying the artifact's arithmetic, not its execution.
- A reported third-party Breakout replication across model generations (Alex Krentsel, X, 2026-11-02: GPT-6 Astra ≈22×, Opus 5.5 ≈20×, GPT-6.1 Sol ≈18× the PPO-500M baseline) — Kingy notes it supplies **no** verification of the Qwen edit or the MATH-500 / IFEval gains.
- Rebuild instructions for the released edit (`exp8_math/code/apply_edit.py` against base revision `2fc06364715b967f1860aea9cf38778875588b17`), with its own "Kingy has not run this command" disclaimer, and the disclosure inventory: missing harness/grader modules, internal paths in eval scripts, omitted intermediate activations and earlier prompt trials.

**Kingy's overall posture** (for the whitepaper's reception section, if one is included): the narrow claim — an agent diagnosed a loop direction in weights and a scaled subtraction recovered large benchmark gains — is unusually concrete and artifact-backed; the broad claims (replacing training, recursive self-improvement, general weight literacy) are not established, the Gemma follow-up and the sycophancy result bound the method, and the decisive next experiment is a controlled comparison against simpler loop controls under matched sampling. This lane concurs with that posture and §1.4 is written to be consistent with it.

**Other secondary coverage seen in this lane (not reviewed in depth, do not cite from this file):** The Register (2026-11-03), a Medium explainer, Artiverse, and a Wikipedia article "Weight-space programming" created after the post. The Wikipedia article's existence is noted only as a reception signal; its critical-coverage pointers (e.g. that the raw-weights-only setting applies only to the small-network experiments) agree with §1.4.6 of this file, which is derived from the primary post itself.

---

## 5. Lane synthesis — what this means for THOX model / device work (brief)

Kept deliberately short; the full THOX programme belongs to the other lanes.

1. **The transferable technique is Exp 8's shape, not its headline:** diagnose a *single-direction failure* (looping, repetition, a stuck behaviour) in a small model's MLP `down_proj` outputs from contrastive productive-vs-pathological activations, subtract the scaled direction from a small set of columns, hash-diff the result, and re-benchmark. That pipeline is model-size-appropriate for THOX edge models (sub-1B to a few B) in a way frontier-scale weight reading is not, and it is reproducible with open tooling — no Astra required for the *edit* itself, only for the open-ended *diagnosis*.
2. **The Gemma control is the design rule:** only attempt a weight-space fix when the failure is a *suppression* failure (truncation, looping, refusal-like blocking of a capability the model demonstrably has when it finishes). If eval failures are ordinary capability errors, expect ~0 gain and spend the effort on training/data instead. Build the "does it finish?" metric (hit-token-limit rate) into THOX evals first — without it, this class of fix is invisible.
3. **Auditing claims must be downgraded to Exp 7's actual result:** weights + attention-pattern auditing of trained-in traits is plausible; weights-only trait/backdoor detection in a real LM is, on this evidence, **not** available. THOX device-model assurance copy must not claim it.
4. **Every THOX weight edit should ship like the HF artifact did:** bit-exact diff against a pinned base revision, sha256 of every changed tensor, an apply script that verifies hashes, a full (not smoke) re-run of the headline benchmark *and* a stated non-replication scope for the rest. That artifact discipline — not the 6× number — is the part of this release most worth copying verbatim.

---

## Sources opened in this lane (2026-11-03)

Primary: rikiyat.github.io/blog/weight-space-programming/ (full text, 515 lines in fetch) · huggingface.co/RikiyaT/Qwen3.5-0.8B-weight-space-programming (+ /tree/main) · huggingface.co/ML-Intern-lab/Qwen3.5-0.8B-weight-space-programming (+ /tree/main) · huggingface.co/spaces/akhaliq/weight-space-programming-demo (metadata shell only — see §1.5 limitation)
Secondary: kingy.ai/blog/weight-space-programming-ai-agent-model-weights (full text)
Corpus: arXiv abstract pages for 2002.05688, 2002.11448, 2209.12892, 2603.10090, 2512.05117, 1609.09106, 2506.06105, 2510.19733, 2202.05262, 2210.07229, 2310.01405, 2106.09685, 2203.05482, 2212.04089, 2306.01708, 2311.03099, 2209.11895, 2301.05062, 2309.03409; transformer-circuits.pub/2021/framework/index.html
