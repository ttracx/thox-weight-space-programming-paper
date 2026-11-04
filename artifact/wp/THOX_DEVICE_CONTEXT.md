# THOX Device Context — Weight-Space Programming Paper

**Lane:** THOX device-model inventory (local sources only)
**Date:** 2026-11-03
**Purpose:** Ground the THOX whitepaper on applying Weight-Space Programming
to THOX device models and ongoing device-model development in the recorded
THOX lineup, bases, gates, quantizations, and device constraints. No model
spec in this file is invented. Anything not found in the searched local
sources is marked **NOT FOUND**.

## Sources consulted (local only)

Primary structured catalog:

- `~/workspace/full-surface-sync-20261102/catalog_live_rev10.json` —
  schemaVersion 3, revision `2026-11-02.1` in the file (file name says rev10),
  reviewedAt 2026-11-01, 94 models. Field names used below: `base`,
  `parametersB`, `downloadGB`, `status`, `producerStatus`, `targets`, `notes`.
  Catalog defaults for published models: formats GGUF + Safetensors,
  quantizations `["Q4_K_M"]` — same file, `defaults.published`.
- `~/workspace/llama-ship-20261103/lane3/hf-ollama-llama-id-map.json` —
  per-model GGUF file names/bytes, gate strings, host tiers, estimated total
  GB at ctx 4096/8192 for the five Phase-1 Llama models (ThoxAir-0.5B,
  ThoxEdge-0.8B, ThoxOS-Kernel-27B, ThoxOS-Kernel-4B, ThoxMini-3B in the
  portion read).
- `~/workspace/hf-model-pages-txfmp/inventory.json` — HF public-model list
  (e.g. ThoxEdge-0.8B, ThoxEdge-0.5B, ThoxMini-3B, ThoxFlux-350M,
  ThoxNano-135M/360M, role models, ThoxMesh family) and collections,
  including "THOX Flagship & Edge Device Models".
- `~/workspace/hf-model-pages-txfmp/cards/<Model>.md` — staged TXF-MP model
  cards, cited per model below.

Program / gate / training records:

- `~/workspace/hf-flagship-20261028/PACK.md`, `RUN.md`, `GATE49.md`,
  `FINISHING.md`, `ENDPOINTS.md`, `SURVEY.md`, `jobs-flagship.yaml` —
  Wave C flagship fine-tune program (2026-10-28/29).
- `~/workspace/thoxos-orangepi-20261103/program/PROGRAM.md` — Orange Pi
  Zero 3W program charter for ThoxMini + ThoxClip (2026-11-03), including
  the locked 2026-10-29 spec-floor mapping.
- `~/workspace/thoxos-orangepi-20261103/lane-f-meshstack-models/MODELS-REVIEW.md`
  — Lane F models review, 2026-11-03, verified against provisioning manifests
  `~/workspace/thox-provisioning-refresh-20261102/manifests/thoxmini-flagship.json`
  and `thoxmini-kernel.json` (catalog rev 2026-11-01.10 + HF LFS metadata).
- `~/workspace/thoxos-orangepi-20261103/lane-f-meshstack-models/MESHSTACK-REVIEW.md`
  — Lane F MeshStack review, 2026-11-03.
- `~/MEMORY.md`, `~/memory/2026-10-27.md`, `~/memory/2026-10-28.md`,
  `~/memory/2026-10-30.md`, `~/memory/2026-11-01.md`, `~/memory/2026-11-03.md`
  — via memory search; citations below give the dated file.
- `~/AGENTS.md` — standing model card rule and Model Catalog Sync Rule
  (see §4).
- Sparks source paper as supplied by the user (for §3 only):
  `~/workspace/user/files/Sparks_of_Weight-Space_Programming_LLMs_can_natively_read___write_neural_network_weights.pdf`
  and the companion note
  `~/workspace/user/files/Creating_frontier_edge_models_and_specific_device_tasks_and_THOX_3.md`,
  which links `RikiyaT/Qwen3.5-0.8B-weight-space-programming` on Hugging Face.

> Catalog discrepancy carried, not hidden: the live website catalog is newer
> than the local catalog copy above. MEMORY.md (2026-11-03 entries) records
> live catalog revision 2026-11-03.2 with 93 models in one pass and 191
> models in the Model Factory catalog in another pass. The per-model facts
> below are from the local rev10 file and the cards/records cited; a fresh
> live-catalog pull is NOT FOUND in local files at the time of this lane.

---

## 1. Device model lineup relevant to weight editing

### 1.1 ThoxAir flagship

#### ThoxAir-0.5B

- Base: `Qwen2.5-0.5B-Instruct` / `Qwen/Qwen2.5-0.5B-Instruct`
  — `catalog_live_rev10.json` (`base: Qwen2.5-0.5B-Instruct`);
  `~/workspace/hf-model-pages-txfmp/cards/ThoxAir-0.5B.md`
  ("Qwen2.5-0.5B-Instruct derivative", merged Wave C.2 adapter).
- Parameters: 0.494 B — `catalog_live_rev10.json`.
- Quantization / files: Q4_K_M GGUF 397,807,584 B (recommended) and
  Q8_0 GGUF 531,067,872 B — `hf-ollama-llama-id-map.json`;
  downloadGB 0.398 (Q4_K_M) — `catalog_live_rev10.json`.
- Device target: `thoxair` — `catalog_live_rev10.json` (`targets: ["thoxair"]`).
  ThoxAir is the 2 GB target class for its config siblings: ThoxAir-Chat-0.5B
  and ThoxAir-Route-0.5B notes say "2 GB target" — same catalog file.
- Status: Published, "Promoted by THOX" — `catalog_live_rev10.json`.
  GATE49 47/49 — same file ("A CTO recall error remains. Promotion is not
  error-free."); card states "PROMOTED — GATE49 47/49, zero known_false
  hard failures", canonical home of the promoted Wave C.2 build —
  `cards/ThoxAir-0.5B.md`.
- History relevant to weight editing: Wave C adapter scored 43/49 and was
  NOT promoted; Wave C.1 scored 42/49, HELD; Wave C.2 scored 47/49,
  PROMOTED — `~/workspace/hf-flagship-20261028/RUN.md`.
- Role in the Mini image: it is also the fallback model in the ThoxMini
  Flagship boot bundle (not only an Air model) — `MODELS-REVIEW.md` §1.

#### ThoxAir-16M-role

- Base: "BitNet b1.58 ternary" — `catalog_live_rev10.json`.
- Parameters: 0.016 B (16M) — same file.
- Quantization: NOT FOUND as a GGUF quant in the catalog; the catalog notes
  the listing states Ollama cannot load the ternary weights for the sibling
  ThoxClip-9M-role (run with llama.cpp) — same file, ThoxClip-9M-role entry.
  For ThoxAir-16M-role itself the catalog notes only "license is pending
  review".
- Device target: `thoxair` — same file.
- Status: Published, workload "Device role research" — same file.
- Lineup role: ThoxAir originally shipped only this role model and "rode
  the 350M tier + mesh"; it had NO queued assistant model, flagged as a gap
  — `~/memory/2026-10-27.md` (edge fast-track inventory, verified from the
  thoxllm-factory registry); `~/workspace/hf-flagship-20261028/jobs-flagship.yaml`
  (air-05b-flagship comment: "Fills the empty ThoxAir flagship slot").

### 1.2 ThoxEdge family — ThoxMini-tier on-device assistants

#### ThoxEdge-0.8B — see also the dedicated verification in §2

- Base: `Qwen3.5-0.8B`, full HF id `Qwen/Qwen3.5-0.8B` —
  `catalog_live_rev10.json` (`base: Qwen3.5-0.8B`);
  `cards/ThoxEdge-0.8B.md` (frontmatter `base_model: Qwen/Qwen3.5-0.8B`,
  heading "Qwen3.5-0.8B derivative").
- Architecture note recorded: "Qwen3.5 is a conditional-generation
  (multimodal) architecture used here text-only; the vision tower is
  untouched by the adapter" — `cards/ThoxEdge-0.8B.md`, Limitations.
  Deeper architecture detail (layers, hidden size, attention type):
  **NOT FOUND** in the local sources searched.
- Parameters: 0.7524 B — `catalog_live_rev10.json`. The card badge says
  0.8B — `cards/ThoxEdge-0.8B.md`. Use 0.7524 B as the catalog figure and
  0.8B as the product name.
- Quantization / files: merged safetensors `model.safetensors`
  1,504,827,608 B; Q4_K_M GGUF 529,297,056 B (recommended, SHA-256
  `8ef0900d…f5625` in the card); Q8_0 GGUF 811,843,232 B —
  `cards/ThoxEdge-0.8B.md`; `hf-ollama-llama-id-map.json`.
  Estimated total 0.9 GB at ctx 4096 / 1.0 GB at ctx 8192 (Q4_K_M) —
  `hf-ollama-llama-id-map.json`.
- Device target: `thoxmini` — `catalog_live_rev10.json`
  (`targets: ["thoxmini"]`). In the Mini image it is the resident routing
  model in BOTH boot bundles — `MODELS-REVIEW.md` §1–§2.
- Status: Published, "Promoted by THOX", GATE49 46/49 —
  `catalog_live_rev10.json`; card: "PASSED the publish bar — GATE49 46/49,
  mean 4.735/5, known_false 10/10, two prefill no-decline hard failures
  remain" — `cards/ThoxEdge-0.8B.md`. Thinking-off required, text-only
  serving — `catalog_live_rev10.json` notes; `MODELS-REVIEW.md` flags
  `thinking_off_required`, `text_only`.

#### ThoxEdge-0.5B

- Base: `Qwen2.5-0.5B-Instruct` / `Qwen/Qwen2.5-0.5B-Instruct` —
  `catalog_live_rev10.json`; `cards/ThoxEdge-0.5B.md`.
- Parameters: 0.5 B — `catalog_live_rev10.json`.
- Quantization / files: Q4_K_M GGUF 397,807,488 B; repo also carries merged
  safetensors and an Ollama Modelfile — `cards/ThoxEdge-0.5B.md`.
  downloadGB 0.398 — `catalog_live_rev10.json`.
- Device targets: `thoxair`, `thoxmini` — `catalog_live_rev10.json`.
  Card summary: "on-device assistant model for the ThoxMini tier: a LoRA
  fine-tune (rank 32) on a THOX-authored corpus of 982 chat, tool-use, and
  factuality examples, merged into the base weights" —
  `cards/ThoxEdge-0.5B.md`.
- Status: Published — `catalog_live_rev10.json`. GATE49 47/49, mean
  4.837/5, 1 hard failure (pricing); card says it "does not pass the gate"
  under the zero-hard-failure policy and is "PUBLISHED, grounding required"
  / published under the Wave B improvement rule —
  `cards/ThoxEdge-0.5B.md`; `~/memory/2026-10-30.md` (README evaluation
  verification entry). Not device-qualified — `catalog_live_rev10.json`.

#### ThoxEdge-4B (explicitly NOT the trained flagship)

- Base: `qwen3:4b` (Qwen3-4B) — `catalog_live_rev10.json`.
- Parameters: 4.0 B; downloadGB 2.5 — same file.
- Status: Published host/laptop configuration; notes state the weights are
  byte-identical to upstream, THOX did not train them, and "Not the trained
  flagship ThoxEdge-0.8B" — same file. Included here only to prevent
  name confusion in the paper.

### 1.3 ThoxMini models

#### ThoxMini-Phi4Mini — the Flagship chat primary

- Base: `Phi-4-mini-instruct` / `microsoft/Phi-4-mini-instruct` —
  `catalog_live_rev10.json`; `~/workspace/hf-flagship-20261028/jobs-flagship.yaml`
  (mini-phi4-flagship, `base_model: microsoft/Phi-4-mini-instruct`).
- Parameters: 3.836 B — `catalog_live_rev10.json`.
- Quantization / files: Q4_K_M GGUF 2,493,840,576 B, SHA-256 `a19e9606…5afedf`;
  downloadGB 2.5 in the catalog — `MODELS-REVIEW.md` §1;
  `catalog_live_rev10.json`.
- Device targets: `thoxmini`, `thoxkey` (it is also the ThoxKey/ThoxBeam
  host flagship payload, because ThoxKey runs no assistant model on-device)
  — `catalog_live_rev10.json`; `jobs-flagship.yaml`.
- Status: Published but "Baseline, not promoted" — `catalog_live_rev10.json`
  ("GATE49 47/49, deployment probe 3/6. Funding fabrication, arithmetic
  and tool-shape defects."); `MODELS-REVIEW.md` §1 repeats BASELINE — NOT
  PROMOTED, GATE49 47/49, probe 3/6. License MIT — same sources.
- Serving contract: ships with the grounded device-facts system prompt,
  never bare — `~/workspace/hf-flagship-20261028/GATE49.md` (6-prompt
  flagship probe section).

#### ThoxMini-3B

- Base: `Llama-3.2-3B` — `catalog_live_rev10.json`. Family in the catalog
  is "Host", distinct from ThoxMini-Phi4Mini.
- Parameters: 3.0 B — same file.
- Quantization / files: Q4_K_M GGUF `thoxmini-3b-Q4_K_M.gguf`
  2,019,373,952 B (from the portion read) — `hf-ollama-llama-id-map.json`;
  downloadGB 2.019 — `catalog_live_rev10.json`. That map records
  "No THOX GATE49 result published for this model".
- Device target: `thoxmini` — `catalog_live_rev10.json`.
- Status: Published — same file. Notes: "Llama-3.2-3B QLoRA fine-tune.
  Public and ungated (2026-10-31); the Llama 3.2 license governs use.
  Distinct from the ThoxMini-Phi4Mini flagship." License `llama3.2` —
  same file.

#### ThoxMini-125M-role

- Base: `ThoxMicro-125M` — `catalog_live_rev10.json`.
- Parameters: 0.125 B — same file.
- Quantization: NOT FOUND in the catalog entry (downloadGB null).
- Device target: `thoxmini`; workload "Device role tasks"; "Full fine-tune
  of ThoxMicro-125M for device-role tasks" — same file.
- Status: Published — same file.

#### ThoxMini config siblings (not THOX-trained)

- ThoxMini-Mind-1.5B: base `Qwen/Qwen2.5-1.5B-Instruct`, 1.5 B, target
  `thoxmini` (4 GB target), "THOX-configured … not THOX-trained" —
  `catalog_live_rev10.json`.
- ThoxMini-Chat-3B: base `Qwen/Qwen2.5-3B-Instruct`, 3.0 B, target
  `thoxmini` (4 GB target), "THOX-configured … not THOX-trained", Qwen
  Research License (non-commercial) — same file.
  These matter for a weight-editing paper because any weight edit would
  change their status from config-only to trained/derivative; today no
  THOX training is claimed for them.

### 1.4 ThoxOS Kernel family

All three entries: `catalog_live_rev10.json`, ThoxOS Kernel family;
GGUF/gate detail also in `hf-ollama-llama-id-map.json`.

#### ThoxOS-Kernel-27B — host-tier teacher

- Base: catalog rev10 says `Qwen3.5-27B`, 27.0 B —
  `catalog_live_rev10.json`.
  **Record discrepancy (do not resolve silently in the paper):**
  MEMORY.md / `~/memory/2026-11-01.md` record that the HF card prints base
  `JonathanColetti/Qwen3.8-27B-Uncensored` in one entry and the website
  entry printed base "Qwen3.5-27B" with a different GATE-K number. The
  local catalog copy is the source used here; the card-vs-catalog base
  discrepancy is flagged in the 2026-11-01 memory entries.
- Training: "THOX-trained full-parameter fine-tune" — `catalog_live_rev10.json`.
- Quantization / files: Q4_K_M GGUF 16,547,400,192 B (downloadGB 16.5);
  Q8_0 GGUF 28,595,763,712 B — `hf-ollama-llama-id-map.json`.
  Host tier "32 GB+ (Q4_K_M); 64 GB (Q8_0)" — same file.
- Device target: none (`targets: []`), host-tier only, not device-qualified,
  "Family teacher and trace source", user-swappable in the ThoxOS
  kernel-model slot — `catalog_live_rev10.json`.
  `MODELS-REVIEW.md` §4: "NEVER [on ThoxMini]. Host only."
- Status: Published under the D11 open-weights ruling; GATE-PASSED under
  the adopted final-answer scoring scope: GATE49 41/49, GATE-K 37/49
  (catalog wording); the raw-completion verdict is HELD and both are
  printed on the card — `catalog_live_rev10.json`;
  `hf-ollama-llama-id-map.json` ("raw-completion verdict HELD — both
  published on card").

#### ThoxOS-Kernel-4B

- Base: `Qwen3.5-4B`, 4.0 B — `catalog_live_rev10.json`.
- Training: "THOX-trained student distilled from ThoxOS-Kernel-27B
  (LoRA fine-tune of Qwen3.5-4B, merged)" — same file.
- Quantization / files: Q4_K_M GGUF 2,708,804,128 B (in MODELS-REVIEW) /
  2,708,804,128 B in the Llama map as 2708804128 B; also Q4_0 and Q8_0
  GGUFs listed — `hf-ollama-llama-id-map.json`; downloadGB 2.7 —
  `catalog_live_rev10.json`.
- Device targets: `thoxmini`, `thoxclip` — `catalog_live_rev10.json`.
  On Mini it is the Boot 2 kernel slot — `MODELS-REVIEW.md` §2.
- Status: Published as a DOCUMENTED BASELINE, NOT gate-passed. GATE49
  44/49; safety bars held (GATE-K known-false hard failure, destructive
  escape, probe escape in the Llama map wording); "deploy only behind a
  harness that enforces destructive-action confirmation" —
  `catalog_live_rev10.json`; `hf-ollama-llama-id-map.json`;
  `MODELS-REVIEW.md` §2 (Boot 2 must not be offered unless the
  destructive-action confirmation harness is present and active).

#### ThoxOS-Kernel-0.8B

- Base: `Qwen3.5-0.8B`, 0.8 B — `catalog_live_rev10.json`.
  This is a second, distinct released model on the same Qwen3.5-0.8B base
  as ThoxEdge-0.8B. `MODELS-REVIEW.md` §6: portal/manifests key by catalog
  id, never by upstream base name, because "two released models share the
  Qwen3.5 0.8B base (Edge vs Kernel-0.8B) and name confusion is a recorded
  defect class"; §4: "never substitute one for the other."
- Training: "THOX-trained student distilled from ThoxOS-Kernel-27B
  (LoRA fine-tune of Qwen3.5-0.8B, merged)" — `catalog_live_rev10.json`.
- Quantization / files: Q4_K_M GGUF 529,297,056 B (same byte size as
  ThoxEdge-0.8B Q4_K_M — different weights, do not confuse the files);
  Q4_0 501,452,448 B; Q8_0 811,843,232 B — `hf-ollama-llama-id-map.json`.
- Device targets: `thoxair`, `thoxkey` — `catalog_live_rev10.json`.
  Summary on its Ollama page (recorded in MEMORY.md 2026-11-01):
  "ThoxOS kernel/OS triage student for ThoxAir and ThoxKey".
- Status: GATE-PASSED: GATE49 37/49, zero hard failures —
  `catalog_live_rev10.json`; `hf-ollama-llama-id-map.json`.
  GATE-K discrepancy on record: catalog rev10 says GATE-K 33/49 in one
  place, MODELS-REVIEW §4 records "GATE-K 33/49 per catalog rev10 vs
  32/49 in the canonical rev — discrepancy still unresolved".
- Weight-editing-relevant serving caveat: the card requires the
  think-suppressed published configuration; raw stock-template serving
  produced final answers in only 1/38 UX prompts, and no verified Llama
  equivalent was found in that lane — `hf-ollama-llama-id-map.json`
  (`servingBlocker`).

### 1.5 ThoxClip / ThoxFlux / ThoxNano

#### ThoxClip-Qwen3-0.6B — the Clip flagship candidate line

- Base: `Qwen3-0.6B` / Qwen3-0.6B — `catalog_live_rev10.json`.
- Parameters: 0.596 B — same file.
- Quantization / files: downloadGB 0.397 (Q4_K_M catalog default);
  Ollama hosts its GGUF build, the HF repo has full safetensors but NO
  GGUF/Modelfile (recorded finishing-lane gap) — `catalog_live_rev10.json`;
  `~/memory/2026-10-31.md` (HF org inventory entry).
- Device target: `thoxclip` — `catalog_live_rev10.json`.
- Status: Published, producerStatus "Baseline, grounding required" —
  same file. Gate history: published build 22/49 (Wave B, weights-only,
  no grounding); held candidates 43/49, 37/49 (CAO ruling), 39/49 in
  later waves — `~/memory/2026-10-30.md`. Catalog notes: "GATE49 22/49
  without serving-side grounding; 14 hard failures. Grounding and
  thinking-off required." Thinking-off: true — `catalog_live_rev10.json`.

#### ThoxFlux-350M

- Base: `LFM2.5-350M` / `LiquidAI/LFM2.5-350M` —
  `catalog_live_rev10.json`; `~/memory/2026-10-27.md`.
- Parameters: 0.35 B — `catalog_live_rev10.json`.
- Quantization / files: downloadGB 0.229 — same file. Specific GGUF quant
  beyond the catalog default Q4_K_M: NOT FOUND in the sources read for
  this model.
- Device target: catalog `targets: []` in rev10 — same file. Earlier
  inventory assigns the ThoxFlux-350M tier to ThoxClip: "ThoxClip =
  ThoxFlux-350M (LFM2.5-350M) + ThoxNano-360M (SmolLM-360M)" —
  `~/memory/2026-10-27.md`; `~/memory/2026-10-28.md`. The paper should
  cite the inventory assignment and note the rev10 catalog leaves
  `targets` empty.
- Status: Published — `catalog_live_rev10.json`. GATE49 20/49, "Wave B
  LoRA … a weak result, stated on its own listing" — same file;
  `~/memory/2026-10-30.md` confirms 20/49 under the Wave B improvement rule.

#### ThoxNano-360M (Clip tier)

- Base: `SmolLM-360M` / `HuggingFaceTB/SmolLM-360M` —
  `catalog_live_rev10.json`; `~/memory/2026-10-27.md`.
- Parameters: 0.36 B; downloadGB 0.271 — `catalog_live_rev10.json`.
- Device target: catalog `targets: []` in rev10; inventory assignment is
  ThoxClip — `~/memory/2026-10-27.md` (same caveat as ThoxFlux-350M).
- Status: Published, Wave B LoRA, GATE49 23/49 (weak result stated on its
  listing) — `catalog_live_rev10.json`.

#### ThoxClip-9M-role

- Base: "BitNet b1.58 ternary" — `catalog_live_rev10.json`.
- Parameters: 0.009 B (9M) — same file.
- Device target: `thoxclip`; workload "Device role research" — same file.
- Status: Published — same file. Note: Ollama cannot load the ternary
  weights; run with llama.cpp — same file.

#### ThoxClip config siblings (not THOX-trained)

- ThoxClip-Mind-1.5B: base `Qwen/Qwen2.5-1.5B-Instruct`, 1.5 B, target
  `thoxclip` (6 GB target), config-only — `catalog_live_rev10.json`.
- ThoxClip-Chat-3B: base `Qwen/Qwen2.5-3B-Instruct`, 3.0 B, target
  `thoxclip` (6 GB target), config-only, Qwen Research License — same file.
- ThoxClip-Agent-4B: base `qwen3:4b`, 4.0 B, target `thoxclip`,
  weights byte-identical to upstream, THOX did not train them — same file.

### 1.6 ThoxKey role and micro models

ThoxKey runs no assistant model on-device (mesh-served); its flagship
payload is ThoxMini-Phi4Mini on the host — see §1.3 and
`~/workspace/hf-flagship-20261028/jobs-flagship.yaml`.

#### ThoxKey-9M-role

- Base: "BitNet ternary" — `catalog_live_rev10.json`.
- Parameters: 0.0089 B (8.9M) — same file.
- Quantization: ternary BitNet checkpoint; GGUF quant NOT FOUND in the
  catalog entry.
- Device target: `thoxkey`; workload "ThoxKey firmware role" — same file.
- Status: Published — same file.

#### ThoxNano-135M (Key tier assistant)

- Base: `SmolLM-135M` / `HuggingFaceTB/SmolLM-135M` —
  `catalog_live_rev10.json`; `~/memory/2026-10-27.md`.
- Parameters: 0.135 B; downloadGB 0.105 — `catalog_live_rev10.json`.
- Device target: `thoxkey` — same file.
- Status: Published, SmolLM-135M LoRA, GATE49 23/49 (weak result stated
  on its listing) — same file.

#### ThoxKey-Micro-0.5B and ThoxKey-Route-0.5B (config-only)

- Base (both): `Qwen/Qwen2.5-0.5B-Instruct`, 0.5 B, downloadGB 0.4,
  target `thoxkey`, published 2026-11-01, "THOX-configured … not
  THOX-trained", 0.59 GB RAM on CPU at 8,192 ctx on the card —
  `catalog_live_rev10.json`.

#### ThoxKey-TLM

- Base: NOT FOUND / no base — its own card proposes retiring it in favour
  of ThoxKey-9M-role; listed as NOT trainable as-is —
  `~/memory/2026-10-27.md`. It appears in the HF public inventory —
  `~/workspace/hf-model-pages-txfmp/inventory.json`. Do not present it as
  a weight-editable candidate without a base.

### 1.7 MeshStack / MeshGroup models

Important framing for the paper, recorded in the catalog itself: most
Mesh models are **configuration-only** — THOX system profile + Knowledge
Pack + serving parameters on upstream weights, explicitly "THOX did not
train these weights" and, for the 30B-A3B family, "MeshStack routes whole
requests to a node; no distributed or split inference is claimed" in the
rev10 notes. The distributed-inference claims belong to the MeshStack
paper line (§4.4), not to these catalog entries.

- ThoxMesh-30B-A3B: base `qwen3:30b-a3b` (Qwen3-30B-A3B, 30.0 B catalog;
  card says 30.5B total, ~3.3B active, MoE), downloadGB 18.6, published,
  config-only — `catalog_live_rev10.json`; `cards/ThoxMesh-30B-A3B.md`
  (base pinned by Ollama digest, 18.56 GB).
- ThoxMesh-Agent-30B, ThoxMesh-MoE-30B, ThoxMeshGroup-30B-A3B: same base
  `qwen3:30b-a3b`, 30.0 B, 18.6 GB, published 2026-11-01, config-only
  with different system profiles — `catalog_live_rev10.json`.
- ThoxMesh-32B: base `Qwen/Qwen3-32B`, 32.0 B, downloadGB 20.2, published
  2026-11-01, "Config-only, not THOX-trained", MeshStack dense baseline —
  same file.
- ThoxMesh-Dense-32B: same base/params, published, config-only — same file.
- ThoxMeshGroup-32B: base `Qwen/Qwen3-32B`, 32.0 B, 20.2 GB, published,
  workgroup assistant, config-only — same file.
- ThoxMesh-Open-14B: base `Qwen/Qwen3-14B`, 14.0 B, 9.28 GB, published,
  config-only — same file.
- ThoxMeshGroup-Federated-8B: base `qwen3:8b`, 8.0 B, 5.23 GB, published,
  config-only; "Federated means site-level request routing only" — same file.
- ThoxMesh-Head-C6: appears in HF inventory — `inventory.json`. Base is a
  placeholder string; NOT trainable as-is — `~/memory/2026-10-27.md`.
  Gate/catalog detail beyond that: NOT FOUND in the sources read.
- ThoxMesh-80B-A3B: status "recipe" (not published), base
  `qwen3-next:80b-a3b-instruct`, 80.0 B — `catalog_live_rev10.json`.

### 1.8 Other weight-relevant device model on record

- ThoxDecide-3B: base `LiquidAI/d1-3B (LFM Open License v1.0)`, 3.12 B,
  status private-trained, "Trained baseline — not promoted", Attempt 3 is
  the version of record (held-out 0.797 vs base 0.695) —
  `catalog_live_rev10.json`. Its Mini device package
  `Thox-ai/ThoxDecide-Mini` (Q4_K_M GGUF 1,674,456,032 B) is INTERNAL-ONLY,
  served only when a device is leased into the ThoxDecide role, and "must
  not be baked into any customer-bound image" — `MODELS-REVIEW.md` §5.
  The ThoxDecide-Air student is a Qwen3-0.6B base, ship quant Q8_0
  (639 MB) because "Q4_K_M quantization itself flipped saturated
  decisions on this small model" — `~/memory/2026-11-03.md`. That
  quantization-sensitivity finding is directly relevant to any
  weight-editing claim on small device models.

---

## 2. Verification: is ThoxEdge-0.8B based on Qwen3.5-0.8B?

**YES — verified in multiple independent local sources.**

The exact model edited in the Sparks paper's Experiment 8 is
Qwen3.5-0.8B: the supplied PDF states in its TL;DR and overview that
Astra was asked to "make Qwen3.5-0.8B better at math", edited 0.016% of
the weights with no gradients/training loop, and raised MATH-500 from
7.9% to 48.1% (with IFEval improving ~3x) —
`~/workspace/user/files/Sparks_of_Weight-Space_Programming_LLMs_can_natively_read___write_neural_network_weights.pdf`
(TL;DR; "In Experiment 8, we ask it to make Qwen3.5-0.8B better at math").
The companion note links the resulting HF repo
`RikiyaT/Qwen3.5-0.8B-weight-space-programming` —
`~/workspace/user/files/Creating_frontier_edge_models_and_specific_device_tasks_and_THOX_3.md`.

ThoxEdge-0.8B's base is the same model, cited from:

1. `~/workspace/hf-model-pages-txfmp/cards/ThoxEdge-0.8B.md` — frontmatter
   `base_model: Qwen/Qwen3.5-0.8B`; heading "ThoxEdge-0.8B — Qwen3.5-0.8B
   derivative"; Training provenance: "Base model: Qwen/Qwen3.5-0.8B
   (Apache-2.0)".
2. `~/workspace/full-surface-sync-20261102/catalog_live_rev10.json` —
   entry `thoxedge-0.8b`: `base: Qwen3.5-0.8B`, `parametersB: 0.7524`.
3. `~/workspace/hf-flagship-20261028/PACK.md` — Wave C table:
   "edge-08b-wavec | Qwen/Qwen3.5-0.8B (Apache-2.0) |
   Thox-ai/ThoxEdge-0.8B-WaveC".
4. `~/workspace/hf-flagship-20261028/RUN.md` — "ThoxEdge-0.8B:
   Qwen/Qwen3.5-0.8B (Apache-2.0) — KEEP".
5. `~/workspace/hf-flagship-20261028/SURVEY.md` — "ThoxEdge-0.8B / Mini
   secondary | KEEP | Qwen/Qwen3.5-0.8B" and "Tier 4 — ThoxEdge-0.8B /
   Mini secondary (0.8B class): KEEP Qwen3.5-0.8B".
6. `~/memory/2026-10-27.md` and `~/memory/2026-10-28.md` — edge fast-track
   inventory: "ThoxEdge-0.8B (Qwen3.5-0.8B)" / "base Qwen/Qwen3.5-0.8B".

Caveat for the paper, recorded in the same sources: ThoxEdge-0.8B is not
the raw base. It is the base plus a THOX QLoRA adapter (r32/alpha 64,
982-row Wave B corpus) merged in bf16 — `cards/ThoxEdge-0.8B.md`. A
weight-space replication on ThoxEdge-0.8B therefore starts from
already-edited (fine-tuned) weights, not from pristine Qwen3.5-0.8B.
The second Qwen3.5-0.8B-derived THOX model, ThoxOS-Kernel-0.8B (§1.4),
is a cleaner "same base, different edit history" comparator: a LoRA
distillation student of the 27B kernel teacher on the identical base.

Also relevant: the Sparks editor model in the paper is named "GPT-6
Astra" in the supplied PDF. Whether any THOX-accessible model has the
same weight-reading ability is NOT FOUND in local sources and must not
be assumed in the paper.

---

## 3. Existing THOX practices that touch weights today

### 3.1 Fine-tuning pipeline (HF Jobs)

- Control plane: `tommytracx/thox-compute` (canonical) dispatches one HF
  Job per fine-tune under the Thox-ai namespace, per-second GPU billing,
  `jobs.yaml` registry, built-in 12-prompt gate + `promote()`; the org
  mirror `Thox-ai/thox-training-control` cannot launch (no secrets) —
  `~/workspace/hf-flagship-20261028/INVENTORY.md`.
- Fleet recipe (Wave B/C, the recipe that produced the promoted builds):
  LoRA r32 / alpha 64, LR 1e-4, cosine, 3 epochs, effective batch 16,
  sequence length 1024, warmup 10 steps (integer), dropout 0.0,
  completion-only loss; corpus `Thox-ai/thox-factory-sft-v5`,
  `train_wave_b.jsonl`, 982 rows (later waves: C.1 1,082 rows, C.2
  1,246 rows) — `~/workspace/hf-flagship-20261028/jobs-flagship.yaml`;
  `~/workspace/hf-flagship-20261028/RUN.md`.
- Output shape: the plane publishes a LoRA adapter (private repo), not
  merged weights. A separate merge step (`merge_and_unload`, bf16) is
  required before GGUF conversion (llama.cpp `convert_hf_to_gguf.py` +
  `llama-quantize`) and Ollama Modelfile packaging —
  `jobs-flagship.yaml`; `cards/ThoxEdge-0.8B.md` (merge job
  6ae3ea17c78863f9c62e160b for Edge-0.8B).
- Job flavours on record: `a10g-small` for 0.5B/0.8B/0.6B entries,
  `a10g-large` for Phi-4-mini (3.8B) — `~/workspace/hf-flagship-20261028/GATE49.md`.
- Trainer repo: `Thox-ai/thox-edge-sft` (`train_edge_sft.py` plus per-model
  run scripts) — `GATE49.md` (premise-correction section).

### 3.2 Gate evaluation — GATE49

- Canonical gate: `scripts/factuality_gate.py` in GitHub repo
  `ttracx/thoxllm-factory`; 49 questions in four categories: verified (12),
  unknown (26), known_false (10), pricing (1); per-question 0–5 trait
  scoring; headline is `passed/49` plus mean; a known-false repetition is
  a hard failure even inside a denial — `~/workspace/hf-flagship-20261028/GATE49.md`.
- Convention: weights-only, no grounding system prompt, so scores stay
  comparable with Wave A/B baselines; the grounded configuration is
  tested separately (Phi-4-mini 6-prompt flagship probe) — same file.
- Publishing authority: the control plane's 12-prompt gate runs first but
  does NOT authorize publishing; GATE49 does. Promotion rule: improve
  over the model's own baseline and never promote with a known_false
  hard failure outstanding; a failed adapter stays in its `-WaveC` repo
  unpublished and the published repo keeps prior weights — same file.
- HF-Job form: gate loads base + adapter with Transformers + PeftModel,
  greedy generation, `enable_thinking=False` for Qwen3/Qwen3.5, writes
  `thox_gate49.json` to the adapter repo and appends a gate banner to
  its card — same file.
- A second gate family exists for the kernel line: GATE-K (Kernel-27B
  37/49 final-answer, Kernel-0.8B 33/49 per catalog with the 32/49
  discrepancy noted in §1.4) — `catalog_live_rev10.json`;
  `MODELS-REVIEW.md` §4.

### 3.3 Model card rule

- Standing rule (Tommy, 2026-10-27): every new model created anywhere
  ships at creation time with a comprehensive model card and README —
  HF frontmatter (license, base model, tags, datasets), summary, intended
  use, training data and procedure, evaluation method and results
  (marked pending honestly until a run lands, then filled), limitations,
  license terms, and provenance (job/run links, registry entry). No
  empty or stub model repos — `~/AGENTS.md`.
- Wave practice confirms it: Wave C.1/C.2 repos were "created private and
  pre-seeded at creation with a comprehensive model card per the model
  card rule", and because trainer publishes overwrote the READMEs, full
  card restoration with the training record + gate results was mandatory
  in the gating step — `~/workspace/hf-flagship-20261028/RUN.md`.
- Completion bar (Wave C, Tommy 2026-10-28): a model is done when it is
  trained AND published, its card is updated with the training record,
  and a whitepaper + documentation package supports it — `~/MEMORY.md`.

### 3.4 Catalog sync rule

- Standing rule (Tommy, 2026-11-01): whenever any THOX model is created,
  updated, promoted, or held, the SAME work updates every surface in one
  pass — THOX Model Factory, model catalogs, all related repositories
  (READMEs/cards/releases), Ollama, and Hugging Face — and prepares the
  matching thox.ai website update; no surface left stale; model-related
  website content is Tommy + Sadie's direct responsibility (Craig gate
  does not apply to model content) — `~/AGENTS.md` (Model Catalog Sync
  Rule, as amended 2026-11-01 09:03 CT).
- A sixth surface was added 2026-11-03: Llama.app / `llama serve` links
  ("Run in Llama") alongside Ollama on HF cards, Model Factory, and
  thox.ai for the five promoted models — `~/MEMORY.md` (Llama.app review
  entry); `~/workspace/llama-ship-20261103/lane3/` (6th-surface spec).
  Any weight-edited re-release must therefore re-sync at least: HF card,
  Ollama, Model Factory/catalog, website catalog, and the Llama ID map.

### 3.5 MeshStack weight / KV sharing

- MeshStack paper line (v1.0.1 public, v1.1.0 evidence edition built
  2026-11-03): "Capacity-Priced Pipeline Sharding, Grant-Gated KV
  Transfer and Lease-Fenced Device Roles for a Private Household Mesh" —
  `~/MEMORY.md` (MeshStack entries).
- KV facts as corrected by the v1.1.0 evidence edition: real-GGUF KV
  compression is 1.17–1.20x, f16, bit-exact; the earlier 1.512x figure
  is restated as a synthetic bf16 harness result and must not be used
  on campaign surfaces; 27B geometry corrected to 65,536 B/token +
  156,894,356 B fixed SSM state — `~/MEMORY.md` (MeshStack v1.1.0 entry).
- Architectural decisions on record: pipeline parallelism is the mesh
  sharding form, tensor parallelism intra-node only, expert parallelism
  reuses shard machinery; MeshStack v2 T3 = grant-gated KV byte transfer
  gated by a PLACE cost model (transfer must beat recompute) —
  `~/memory/2026-10-30.md` (CAO decisions D9–D12).
- What the mesh does NOT share: for Apple Foundation Models, the mesh
  shares ACCESS, not model weights (OS + Apple Account bound, PCC quota
  per account, iOS nodes consumers only) — `~/memory/2026-10-25.md`.
- Auto Device Role mode (deployed internally 2026-11-02): a coordinator
  leases a pool device to serve a role payload (model GGUF, hash-verified
  by `model_fp` SHA-256 in the serve config), then drains it back to the
  pool; lease TTL 300 s; owner priority (owner foreground work is never
  evicted) — `MESHSTACK-REVIEW.md` §1. This is the existing mechanism a
  weight-edited payload would ride: payloads are content-addressed,
  hash-checked, and swapped by lease, never edited in place on a device.
- Catalog-level honesty: the published Mesh/MeshGroup models in §1.7 are
  config-only on upstream weights; no split/distributed inference is
  claimed for them in the catalog — `catalog_live_rev10.json`.

---

## 4. Constraints for on-device weight updates

### 4.1 Device RAM / storage floors (locked spec floors, 2026-10-29)

Source: `~/workspace/thoxos-orangepi-20261103/program/PROGRAM.md` §2.1
(spec-floor mapping against THOX Device Spec Floors, locked 2026-10-29),
cross-checked in `~/MEMORY.md` (Orange Pi program entry).

| Device / floor | Floor | Recommended / SKU note |
|---|---|---|
| ThoxMini — P4 | 4 GB LPDDR5+ minimum; 8-core hybrid (2 perf @ 2.0 GHz+ + 6 eff); NPU 3 TOPS INT8+; Wi-Fi 6 / BT 5.0+; flash to 256 GB | 8 GB recommended ("headroom for 3B Q4 + services") — PROGRAM.md §2.1 |
| ThoxClip — P6 | Same compute floors as Mini, 6 GB LPDDR5+ | 6 GB SKU if procurable, else 8 GB SKU — PROGRAM.md §2.1 |
| ThoxAir — E2 class | 2 GB target (from the Air config-model notes, "2 GB target") | Design ranking on record: Clip P6 (6 GB) > Mini P4 (4 GB) > Air E2 (2 GB) — `~/memory/2026-10-30.md`. A formal E2 floor table entry: NOT FOUND in the Orange Pi charter (it covers Mini/Clip only). |
| ThoxKey | No assistant model on-device; host/mesh-served flagship | Floor values for the Key board itself: NOT FOUND in the sources searched for this lane. |

Board that meets P4/P6 with no waiver: Orange Pi Zero 3W (Allwinner A733,
2x A76 @ 2.0 GHz + 6x A55, 3 TOPS NPU, LPDDR5 SKUs 1/2/4/6/8/12/16 GB,
microSD to 128 GB + optional eMMC/UFS, PCIe NVMe option for 256 GB) —
`PROGRAM.md` §2–§2.1. Reference hardware in hand: 12 GB SKU + 256 GB
microSD on KnightHub — `PROGRAM.md` §7, §9; `~/MEMORY.md`.
Warning on record: Orange Pi Zero 3 (H618) is a different, weaker board —
never substitute — `PROGRAM.md` §2.

RAM-fit facts that bound weight updates:

- Shipped policy stays the 4 GB-floor policy for Mini even though the
  reference unit is 12 GB: "images must not silently require the 12 GB
  unit" — `MODELS-REVIEW.md` §3.
- Flagship resident set on Mini = Phi4Mini Q4_K_M (2.49 GB file) + Edge
  routing model, per-boot by design — `MODELS-REVIEW.md` §3.
- ThoxDecide decision seat on Mini-class hardware: Q4_K_M resident
  ≈ 2,886 MB with ~1,210 MB headroom on a 4 GB unit; chat is an on-demand
  swap, never co-resident with the decision seat — `MESHSTACK-REVIEW.md` §1.
- ThoxDecide-Air student full stack: 1,347 MB resident of ThoxAir's
  2,048 MB (701 MB headroom) at its Q8_0 ship quant — `~/memory/2026-11-03.md`.
- Dual-boot model bytes on Mini: unique bytes across both boots
  6,127,749,344 B (≈ 6.13 GB, Edge deduplicated); planning total with
  staging + full rollback reserve ≈ 15 GB — `MODELS-REVIEW.md` §3.

### 4.2 Storage layout for models on the Mini image

- 256 GB budget from the program decisions: ~2.5 GiB boot/recovery,
  16 GiB rootfs slots, 32 GiB models, ~187 GiB data — `PROGRAM.md` §11.
- Model store design: a separate `models` partition holding a
  content-addressed store (`<sha256>.gguf`, mounted read-only; **the
  updater is the only writer, via staging**), per-boot manifests
  `manifests/mini-flagship.MODELS.json` / `manifests/mini-kernel.MODELS.json`,
  shared `/data` (identity/settings/onboarding/chat/boot/logs) —
  `MODELS-REVIEW.md` §3.
- Implication for weight-space edits: an on-device weight edit cannot
  write the read-only model store directly under the current design; it
  would have to land as a new content-addressed artifact through the
  updater/staging path, with a new manifest entry. A direct in-place
  weight-mutation mechanism on device: **NOT FOUND** in local sources.

### 4.3 Update / OTA mechanisms on record

- A/B update + rollback: RAUC templates from thoxos-core; charter
  acceptance gate 6 requires "A/B update + rollback demonstrated (RAUC
  templates from thoxos-core)" — `PROGRAM.md` §4 (Lane B), §6.
- Boot flow: U-Boot with A/B RAUC slots and verified-boot posture —
  `PROGRAM.md` §4 (Lane B scope).
- Dual boot (G-1, decided 2026-11-02): Boot 1 Flagship bundle, Boot 2
  Kernel bundle, one shared rootfs, A/B boot profiles, shared /data;
  Boot 2 requires the destructive-action confirmation harness (which
  does not yet exist as a shipped component, so Boot 2 is not offered
  until it does) — `PROGRAM.md` §9, §11.
- First-boot provisioning: consumes `thox-provision.yaml` once, archives
  it 0600, removes it from the boot partition (standing contract) —
  `PROGRAM.md` §6 (gate 4).
- Manifest signing: the G-1 dual-boot manifests are UNSIGNED (catalog
  rev 2026-11-01.10); signing is an unbuilt workstream and blocks any
  "release" label on a flashed image — `PROGRAM.md` §11;
  `MODELS-REVIEW.md` §7.
- Model-slot swapping already exists as a concept: the kernel model is
  user-swappable in the ThoxOS kernel-model slot (Kernel-27B entry) —
  `catalog_live_rev10.json`. A general OTA channel for pushing a single
  weight-edited GGUF to shipped customer devices (beyond the RAUC image
  path and the fleet-internal role-payload lease path in §3.5):
  **NOT FOUND** in local sources.

### 4.4 Serving constraints that a weight edit must preserve

- Ship quants are the gate-measured artifacts; do not re-quantize —
  `MODELS-REVIEW.md` §6, citing the precedent that Q4_K_M quantization
  flipped saturated ThoxDecide decisions and that re-quantize-to-fit was
  rejected in G-1 Option C. Any weight-space edit therefore has to be
  re-gated at the exact ship quant (Q4_K_M for most, Q8_0 for the
  ThoxDecide-Air student).
- Thinking-off is part of the measured configuration for ThoxEdge-0.8B,
  ThoxClip-Qwen3-0.6B, and ThoxOS-Kernel-0.8B — `catalog_live_rev10.json`;
  `hf-ollama-llama-id-map.json`.
- Engine on the A733 board: llama.cpp `llama-server` built for
  aarch64/A733 (binaries are host-CPU-specific; a copied binary SIGILL'd
  on another host in fleet experience); CPU inference on A76/A55; NPU
  and PowerVR GPU offload are not part of the serving path and are not
  claimed — `MODELS-REVIEW.md` §6; `MESHSTACK-REVIEW.md` §2.
- Identity rule: models are keyed by catalog id, never by upstream base
  name (two released models share the Qwen3.5-0.8B base) —
  `MODELS-REVIEW.md` §6.

---

## 5. NOT FOUND summary (do not fill these in by inference)

- Deeper architecture details (layer counts, hidden sizes, attention/SSM
  layout) for any THOX device model, beyond the Qwen3.5
  conditional-generation note for ThoxEdge-0.8B in §1.2.
- A GGUF quant for ThoxFlux-350M, ThoxMini-125M-role, ThoxKey-9M-role,
  or ThoxClip-9M-role beyond the catalog default / ternary descriptions
  cited.
- A GATE49 result for ThoxMini-3B (explicitly "No THOX GATE49 result
  published for this model" in the Llama ID map).
- A base model for ThoxKey-TLM (none recorded) or for ThoxMesh-Head-C6
  (placeholder string recorded).
- A formal ThoxKey hardware floor table and a formal ThoxAir E2 floor
  table in the Orange Pi charter (Air's 2 GB target comes from catalog
  notes and the 2026-10-30 ranking entry).
- Any existing on-device, in-place weight-mutation mechanism, and any
  customer-device OTA channel for single-model GGUF updates beyond the
  RAUC A/B image path and the fleet-internal MeshStack role-lease path.
- Any local evidence that a THOX-accessible LLM can perform Sparks-style
  native weight reading/editing; the Sparks editor ("GPT-6 Astra") is
  external to the THOX fleet on the local record.
- A fresh live catalog pull newer than the local rev10 copy (live
  revision 2026-11-03.2 is recorded in MEMORY.md but its JSON is not in
  the local files searched).

## 6. One-line takeaway for the paper

THOX already ships a promoted, GATE49-measured derivative
(ThoxEdge-0.8B, 46/49) of the exact base model the Sparks paper edits in
Experiment 8 (Qwen3.5-0.8B), plus a second same-base derivative
(ThoxOS-Kernel-0.8B, GATE-PASSED 37/49) — giving the THOX program a
ready-made, gate-instrumented testbed for weight-space editing, provided
edits are treated as new trained artifacts: re-quantized only at the
ship quant, re-gated by GATE49, re-carded, catalog-synced on all
surfaces, and delivered through the content-addressed, updater-only
model store rather than mutated in place.
