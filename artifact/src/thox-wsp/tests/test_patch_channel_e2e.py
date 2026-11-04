"""End-to-end patch channel test (whitepaper lifecycle steps 1-6):
Python toolkit fingerprints a base tensor, builds + signs a rank-1
manifest; the Rust loader verifies the signature, checks the base hash,
applies into slot B, verifies the result hash, switches; rollback
restores slot A. Also: a tampered manifest must fail verification and a
wrong base must abort the apply.
Run: python3 tests/test_patch_channel_e2e.py  (needs cargo build first)
"""
import hashlib, json, struct, subprocess, sys, tempfile
from pathlib import Path
import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from wsp.manifest import Manifest, PatchOp
from wsp.sign import generate_keypair, sign_manifest, verify_manifest
from wsp.rank1 import apply_rank1

BIN = ROOT / "rust/thox-patch-loader/target/debug/thox-patch-loader"
TENSOR = "model.layers.0.mlp.down_proj.weight"

def f32_to_bf16_bytes(a: np.ndarray) -> bytes:
    # numpy float32 -> bf16 via ml_dtypes if present, else bit trick (RNE)
    try:
        import ml_dtypes  # noqa
        return a.astype("bfloat16").tobytes()
    except ImportError:
        u = a.view(np.uint32).astype(np.uint64)
        lsb = (u >> 16) & 1
        r = ((u + 0x7FFF + lsb) >> 16).astype(np.uint16)
        return r.tobytes()

def main():
    assert BIN.exists(), "build the Rust loader first: cargo build"
    rng = np.random.default_rng(9)
    W = rng.normal(0, 0.4, (8, 16)).astype(np.float32)
    u = rng.normal(0, 1, 8).astype(np.float32)
    cols, alpha = [2, 5, 9, 11], 6.0
    # expected result computed in bf16 space like the loader: decode the
    # bf16 base back to f32, apply, re-encode
    base_bytes = f32_to_bf16_bytes(W)
    W_bf = np.frombuffer(base_bytes, dtype=np.uint16).astype(np.uint32)
    W_dec = (W_bf << 16).view(np.float32).reshape(8, 16).copy()
    exp = apply_rank1(W_dec, u, cols, alpha)
    exp_bytes = f32_to_bf16_bytes(exp)

    priv, pub = generate_keypair()
    base_hash = hashlib.sha256(base_bytes).hexdigest()
    man = Manifest(
        base_repo="Thox-ai/test-model", base_revision="deadbeef",
        base_tensor_sha256={TENSOR: base_hash},
        ops=[PatchOp(tensor=TENSOR, u=[float(x) for x in u], cols=cols,
                     alpha=alpha, dtype="bfloat16")],
        result_tensor_sha256={TENSOR: hashlib.sha256(exp_bytes).hexdigest()},
        eval_report_sha256="0" * 64,
        editor={"model_id": "test-editor", "effort": "unit"},
        license={"base": "Apache-2.0", "patch": "Apache-2.0"})
    sign_manifest(man, priv)
    assert verify_manifest(man, pub)

    with tempfile.TemporaryDirectory() as td:
        td = Path(td)
        store = td / "store"; slot_a = store / "slots" / "A"
        slot_a.mkdir(parents=True)
        (slot_a / (TENSOR.replace("/", "__") + ".bin")).write_bytes(base_bytes)
        (store / "active.txt").write_text("A")
        (td / "pub.bin").write_bytes(pub)
        mp = td / "manifest.json"; mp.write_text(man.to_json())
        shapes = td / "shapes.json"; shapes.write_text(json.dumps({TENSOR: [8, 16]}))

        def run(*a):
            r = subprocess.run([str(BIN), *a], capture_output=True, text=True)
            return r.returncode, (r.stdout + r.stderr).strip()

        rc, out = run("verify", "--manifest", str(mp), "--pubkey", str(td / "pub.bin"))
        assert rc == 0, out; print("verify:", out)
        rc, out = run("apply", "--manifest", str(mp), "--pubkey", str(td / "pub.bin"),
                      "--store", str(store), "--shapes", str(shapes))
        assert rc == 0, out; print("apply:", out)
        got = (store / "slots" / "B" / (TENSOR.replace("/", "__") + ".bin")).read_bytes()
        assert got == exp_bytes, "applied tensor != Python-computed result"
        print("applied tensor is bit-identical to the Python reference result")
        rc, out = run("rollback", "--store", str(store))
        assert rc == 0 and "active slot is now A" in out, out; print("rollback:", out)
        # tamper: change alpha after signing
        bad = json.loads(man.to_json()); bad["ops"][0]["alpha"] = "7.0"
        bp = td / "bad.json"; bp.write_text(json.dumps(bad))
        rc, out = run("verify", "--manifest", str(bp), "--pubkey", str(td / "pub.bin"))
        assert rc != 0 and "FAILED" in out, out; print("tamper correctly rejected:", out)
        # wrong base: corrupt slot A tensor, apply must abort on base hash
        (slot_a / (TENSOR.replace("/", "__") + ".bin")).write_bytes(b"\x00" * len(base_bytes))
        rc, out = run("apply", "--manifest", str(mp), "--pubkey", str(td / "pub.bin"),
                      "--store", str(store), "--shapes", str(shapes))
        assert rc != 0 and "BASE HASH MISMATCH" in out, out
        print("wrong base correctly aborted:", out)
    print("PATCH CHANNEL E2E: ALL PASS")

if __name__ == "__main__":
    main()
