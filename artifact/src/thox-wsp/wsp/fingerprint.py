"""Base-model fingerprinting: per-tensor SHA-256 over raw tensor bytes."""
import hashlib, json
from pathlib import Path

def tensor_sha256(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()

def fingerprint_safetensors(path: str) -> dict:
    from safetensors import safe_open
    out = {}
    with safe_open(path, framework="numpy") as f:
        for name in f.keys():
            t = f.get_tensor(name)
            out[name] = {"sha256": tensor_sha256(t.tobytes()),
                         "shape": list(t.shape), "dtype": str(t.dtype)}
    return out

def fingerprint_file(path: str) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()
