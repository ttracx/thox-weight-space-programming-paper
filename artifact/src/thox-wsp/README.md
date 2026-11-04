# thox-wsp: THOX Weight-Space Programming toolkit

Diagnose, patch, sign and verify small weight edits for THOX device
models. Built for the THOX WSP whitepaper v1.0.0 program: the LLM editor
proposes, deterministic tools measure, edit, hash and gate.

## Python toolkit (`wsp/`)
- `fingerprint.py` per-tensor SHA-256 of a base checkpoint.
- `rank1.py` rank-1 edits in factor form (the Experiment 8 patch shape)
  plus a diff factoriser that audits third-party edits.
- `manifest.py` patch manifest v1 (signed contract; floats ship as bit
  patterns, never JSON numbers).
- `sign.py` Ed25519 signing/verification (release key stays outside the
  editing environment).
- `circuits.py` weight-reading tools from the recreation experiments.
- `loopmetrics.py` n-gram loop and cap-hit metrics for baselines.

## Rust loader (`rust/thox-patch-loader/`)
Verifies the Ed25519 signature and base-tensor hashes, applies the
rank-1 ops into the inactive A/B slot, verifies result hashes, then
atomically switches. `rollback` flips back. Std-safe dependencies only
(sha2, ed25519-dalek, serde_json).

    cargo build --offline
    cargo test --offline          # includes the Python cross-check vector
    python3 tests/test_patch_channel_e2e.py   # full lifecycle, both languages

## Status
v0.1.0, 2026-11-03. Patch channel end-to-end test passes. No production
patch has been issued through this channel yet.
