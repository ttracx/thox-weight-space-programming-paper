"""Patch manifest v1: the signed contract between editor and device.

Wire-form rule (field lesson, 2026-11-03): floats never appear as JSON
numbers in a manifest. `u` ships as hex of its little-endian float32
bytes and `alpha` as a decimal string. Python's repr and Rust's ryu
disagree in the last digit on some floats, and serde_json's number
parser can land 1 ulp away from Python's parser; a signature over
either formatting is not portable. Bit patterns are.
"""
import hashlib, json, struct
from dataclasses import dataclass, field, asdict

SCHEMA = "thox-wsp/patch-manifest/v1"

@dataclass
class PatchOp:
    tensor: str
    formula: str = "rank1_v1"
    u: list = field(default_factory=list)
    cols: list = field(default_factory=list)
    alpha: float = 0.0
    dtype: str = "bfloat16"

@dataclass
class Manifest:
    base_repo: str
    base_revision: str
    base_tensor_sha256: dict
    ops: list
    result_tensor_sha256: dict
    eval_report_sha256: str = ""
    editor: dict = field(default_factory=dict)
    license: dict = field(default_factory=dict)
    schema: str = SCHEMA
    signature: str = ""

    def wire_dict(self) -> dict:
        d = asdict(self)
        for op in d["ops"]:
            u = op.pop("u")
            op["u_hex"] = b"".join(struct.pack("<f", float(x)) for x in u).hex()
            op["alpha"] = repr(float(op["alpha"]))
        return d

    def canonical_bytes(self) -> bytes:
        d = self.wire_dict(); d.pop("signature", None)
        def no_floats(x):
            if isinstance(x, float):
                raise ValueError("bare float in canonical manifest")
            if isinstance(x, dict):
                for v in x.values(): no_floats(v)
            if isinstance(x, list):
                for v in x: no_floats(v)
        no_floats(d)
        return json.dumps(d, sort_keys=True, separators=(",", ":")).encode()

    def digest(self) -> str:
        return hashlib.sha256(self.canonical_bytes()).hexdigest()

    def to_json(self) -> str:
        return json.dumps(self.wire_dict(), indent=1)

    @staticmethod
    def from_json(text: str) -> "Manifest":
        d = json.loads(text)
        ops = []
        for op in d["ops"]:
            raw = bytes.fromhex(op.pop("u_hex"))
            op["u"] = list(struct.unpack(f"<{len(raw)//4}f", raw))
            op["alpha"] = float(op["alpha"])
            ops.append(PatchOp(**op))
        d["ops"] = ops
        return Manifest(**d)
