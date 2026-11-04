# Quickstart

```bash
# Experiments (numpy only for E1-E3; torch venv for E4/E0)
python3 artifact/exp/wsp_experiments.py
python3 artifact/exp/e0_rebuild.py        # downloads pinned tensors

# Patch channel
cd artifact/src/thox-wsp/rust/thox-patch-loader && cargo test --offline
python3 artifact/src/thox-wsp/tests/test_patch_channel_e2e.py

# Paper
python3 artifact/wp/build.py && python3 artifact/wp/build_demo.py
python3 artifact/wp/validate.py           # expect: ALL PASS
```

Every number in the paper traces to `artifact/exp/results/summary.json`
and its companion result files.
