//! thox-patch-loader: verify and apply THOX WSP rank-1 weight patches.
//!
//! Safety contract (THOX WSP whitepaper, patch lifecycle):
//! 1. The manifest is Ed25519-signed; verification happens before any
//!    tensor is touched.
//! 2. Every base tensor is pinned by SHA-256 in the manifest. A base
//!    mismatch aborts the apply.
//! 3. The patch is applied into the INACTIVE A/B slot only.
//! 4. Every resulting tensor is hashed and compared with the manifest's
//!    result hashes before the atomic switch.
//! 5. Rollback is a pointer flip back to the previous slot.
//!
//! Tensor files are raw little-endian bytes (f32 or bf16) in a slot
//! directory, one file per tensor, named by the tensor's manifest key
//! with '/' replaced by '__'.

use ed25519_dalek::{Signature, Verifier, VerifyingKey};
use serde::Deserialize;
use sha2::{Digest, Sha256};
use std::collections::BTreeMap;
use std::path::{Path, PathBuf};

#[derive(Debug, Clone, Deserialize)]
pub struct PatchOp {
    pub tensor: String,
    pub formula: String,
    /// Factor vector as hex of little-endian float32 bytes (wire form;
    /// JSON floats are not bit-stable across languages).
    pub u_hex: String,
    pub cols: Vec<usize>,
    /// Decimal string, parsed as data (never a JSON number).
    pub alpha: String,
    pub dtype: String,
}

impl PatchOp {
    pub fn u(&self) -> Result<Vec<f64>, String> {
        let raw = hex::decode(&self.u_hex).map_err(|_| "u_hex is not hex")?;
        if raw.len() % 4 != 0 { return Err("u_hex length not a multiple of 4".into()) }
        Ok(raw.chunks_exact(4)
            .map(|c| f32::from_le_bytes([c[0], c[1], c[2], c[3]]) as f64).collect())
    }
    pub fn alpha(&self) -> Result<f64, String> {
        self.alpha.parse::<f64>().map_err(|_| "alpha is not a decimal string".into())
    }
}

#[derive(Debug, Clone, Deserialize)]
pub struct Manifest {
    pub schema: String,
    pub base_repo: String,
    pub base_revision: String,
    pub base_tensor_sha256: BTreeMap<String, String>,
    pub ops: Vec<PatchOp>,
    pub result_tensor_sha256: BTreeMap<String, String>,
    #[serde(default)]
    pub eval_report_sha256: String,
    #[serde(default)]
    pub editor: serde_json::Value,
    #[serde(default)]
    pub license: serde_json::Value,
    pub signature: String,
}

pub fn sha256_hex(bytes: &[u8]) -> String {
    let mut h = Sha256::new();
    h.update(bytes);
    hex::encode(h.finalize())
}

/// Canonical manifest bytes: the signed payload. Mirrors the Python
/// toolkit (`wsp/manifest.py`): JSON with the `signature` field removed,
/// keys sorted, compact separators.
pub fn canonical_bytes(manifest_json: &str) -> Result<Vec<u8>, String> {
    let mut v: serde_json::Value =
        serde_json::from_str(manifest_json).map_err(|e| format!("manifest parse: {e}"))?;
    let obj = v.as_object_mut().ok_or("manifest is not an object")?;
    obj.remove("signature");
    serde_json::to_vec(&v).map_err(|e| format!("canonical serialize: {e}"))
}

pub fn verify_signature(manifest_json: &str, pubkey: &[u8; 32]) -> Result<Manifest, String> {
    let m: Manifest =
        serde_json::from_str(manifest_json).map_err(|e| format!("manifest parse: {e}"))?;
    if m.schema != "thox-wsp/patch-manifest/v1" {
        return Err(format!("unsupported schema {}", m.schema));
    }
    let sig_bytes = hex::decode(&m.signature).map_err(|_| "signature is not hex")?;
    let sig = Signature::from_slice(&sig_bytes).map_err(|_| "bad signature length")?;
    let key = VerifyingKey::from_bytes(pubkey).map_err(|_| "bad public key")?;
    let canon = canonical_bytes(manifest_json)?;
    key.verify(&canon, &sig).map_err(|_| "signature verification FAILED")?;
    Ok(m)
}

// ---------------------------------------------------------------- bf16
pub fn bf16_to_f32(bits: u16) -> f32 {
    f32::from_bits((bits as u32) << 16)
}

/// f32 -> bf16 with round-to-nearest-even (matches NumPy/ml_dtypes).
pub fn f32_to_bf16(x: f32) -> u16 {
    let bits = x.to_bits();
    let lsb = (bits >> 16) & 1;
    let rounded = bits.wrapping_add(0x7FFF + lsb);
    (rounded >> 16) as u16
}

// ------------------------------------------------------------- rank-1 op
/// Apply one rank1_v1 op to a row-major (rows x cols_total) tensor held
/// as f32 values: W[:, cols] -= alpha * outer(u, u @ W[:, cols]).
pub fn apply_rank1_f32(w: &mut [f32], rows: usize, cols_total: usize, op: &PatchOp) {
    assert_eq!(op.formula, "rank1_v1");
    let u = op.u().expect("decode u");
    let alpha = op.alpha().expect("parse alpha");
    assert_eq!(u.len(), rows, "u length must equal tensor rows");
    let mut proj = vec![0.0f64; op.cols.len()];
    for (j, &c) in op.cols.iter().enumerate() {
        let mut acc = 0.0f64;
        for r in 0..rows {
            acc += u[r] * w[r * cols_total + c] as f64;
        }
        proj[j] = acc;
    }
    for (j, &c) in op.cols.iter().enumerate() {
        for r in 0..rows {
            let nv = w[r * cols_total + c] as f64 - alpha * u[r] * proj[j];
            w[r * cols_total + c] = nv as f32;
        }
    }
}

/// Decode a raw tensor file to f32 values per its dtype tag.
pub fn decode_tensor(bytes: &[u8], dtype: &str) -> Result<Vec<f32>, String> {
    match dtype {
        "float32" => {
            if bytes.len() % 4 != 0 { return Err("f32 tensor byte length".into()) }
            Ok(bytes.chunks_exact(4)
                .map(|c| f32::from_le_bytes([c[0], c[1], c[2], c[3]])).collect())
        }
        "bfloat16" => {
            if bytes.len() % 2 != 0 { return Err("bf16 tensor byte length".into()) }
            Ok(bytes.chunks_exact(2)
                .map(|c| bf16_to_f32(u16::from_le_bytes([c[0], c[1]]))).collect())
        }
        other => Err(format!("unsupported dtype {other}")),
    }
}

pub fn encode_tensor(vals: &[f32], dtype: &str) -> Vec<u8> {
    match dtype {
        "float32" => vals.iter().flat_map(|v| v.to_le_bytes()).collect(),
        "bfloat16" => vals.iter().flat_map(|v| f32_to_bf16(*v).to_le_bytes()).collect(),
        _ => unreachable!(),
    }
}

// --------------------------------------------------------------- A/B slots
pub struct SlotStore {
    pub root: PathBuf,
}

pub fn tensor_filename(tensor: &str) -> String {
    format!("{}.bin", tensor.replace('/', "__"))
}

impl SlotStore {
    pub fn open(root: &Path) -> Self {
        SlotStore { root: root.to_path_buf() }
    }
    pub fn slot_dir(&self, slot: &str) -> PathBuf {
        self.root.join("slots").join(slot)
    }
    pub fn active_slot(&self) -> String {
        std::fs::read_to_string(self.root.join("active.txt"))
            .map(|s| s.trim().to_string())
            .unwrap_or_else(|_| "A".to_string())
    }
    fn flip_active(&self, slot: &str) -> Result<(), String> {
        let tmp = self.root.join("active.txt.tmp");
        std::fs::write(&tmp, slot).map_err(|e| e.to_string())?;
        std::fs::rename(&tmp, self.root.join("active.txt")).map_err(|e| e.to_string())?;
        Ok(())
    }
    pub fn rollback(&self) -> Result<String, String> {
        let cur = self.active_slot();
        let other = if cur == "A" { "B" } else { "A" };
        if !self.slot_dir(other).exists() {
            return Err(format!("slot {other} does not exist; nothing to roll back to"));
        }
        self.flip_active(other)?;
        Ok(other.to_string())
    }

    /// Full apply: verify base hashes in the active slot, write patched
    /// tensors into the inactive slot, verify result hashes, flip.
    /// `shapes` maps tensor name -> (rows, cols).
    pub fn apply(
        &self,
        m: &Manifest,
        shapes: &BTreeMap<String, (usize, usize)>,
    ) -> Result<String, String> {
        let active = self.active_slot();
        let inactive = if active == "A" { "B" } else { "A" };
        let src = self.slot_dir(&active);
        let dst = self.slot_dir(inactive);
        std::fs::create_dir_all(&dst).map_err(|e| e.to_string())?;

        // copy-on-write: start the inactive slot as a copy of active
        for (tensor, want_hash) in &m.base_tensor_sha256 {
            let bytes = std::fs::read(src.join(tensor_filename(tensor)))
                .map_err(|e| format!("read base tensor {tensor}: {e}"))?;
            if sha256_hex(&bytes) != *want_hash {
                return Err(format!("BASE HASH MISMATCH for {tensor}; aborting"));
            }
            std::fs::write(dst.join(tensor_filename(tensor)), &bytes)
                .map_err(|e| e.to_string())?;
        }
        // apply ops in the inactive slot
        for op in &m.ops {
            let (rows, cols) = shapes
                .get(&op.tensor)
                .ok_or_else(|| format!("no shape for {}", op.tensor))?;
            let path = dst.join(tensor_filename(&op.tensor));
            let bytes = std::fs::read(&path).map_err(|e| e.to_string())?;
            let mut vals = decode_tensor(&bytes, &op.dtype)?;
            if vals.len() != rows * cols {
                return Err(format!("shape mismatch for {}", op.tensor));
            }
            apply_rank1_f32(&mut vals, *rows, *cols, op);
            std::fs::write(&path, encode_tensor(&vals, &op.dtype))
                .map_err(|e| e.to_string())?;
        }
        // verify result hashes before switching
        for (tensor, want_hash) in &m.result_tensor_sha256 {
            let bytes = std::fs::read(dst.join(tensor_filename(tensor)))
                .map_err(|e| e.to_string())?;
            if sha256_hex(&bytes) != *want_hash {
                return Err(format!("RESULT HASH MISMATCH for {tensor}; not switching"));
            }
        }
        self.flip_active(inactive)?;
        Ok(inactive.to_string())
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn bf16_roundtrip_and_rne() {
        for v in [0.0f32, 1.0, -2.5, 3.14159, 0.1, -0.7] {
            let back = bf16_to_f32(f32_to_bf16(v));
            assert!((back - v).abs() / v.abs().max(1.0) < 0.01, "{v} -> {back}");
        }
        // exact bf16 values round-trip bit-exactly
        assert_eq!(f32_to_bf16(1.0), 0x3F80);
        assert_eq!(bf16_to_f32(0x3F80), 1.0);
    }

    #[test]
    fn rank1_matches_python_toolkit_vector() {
        // Test vector generated by wsp/rank1.py (NumPy float64 path),
        // seed 42: W is 4x6 f32, u len 4, cols [1,3,4], alpha 6.
        let w0: [f32; 24] = [
            0.15235855, -0.51999205, 0.37522560, 0.47028235, -0.97551757, -0.65108973,
            0.06392020, -0.15812130, -0.00840058, -0.42652196, 0.43969899, 0.38889596,
            0.03301535, 0.56362063, 0.23375466, -0.42964622, 0.18437539, -0.47944131,
            0.43922514, -0.02496296, -0.09243118, -0.34046477, 0.61127067, -0.07726474,
        ];
        let expect: [f32; 24] = [
            0.15235855, 0.94310236, 0.37522560, -0.56892949, 0.52672708, -0.65108973,
            0.06392020, 1.04470646, -0.00840058, -1.28087068, 1.67471266, 0.38889596,
            0.03301535, -1.25465620, 0.23375466, 0.86184585, -1.68255591, -0.47944131,
            0.43922514, -1.27325726, -0.09243118, 0.54617804, -0.67042607, -0.07726474,
        ];
        let u_hex = [-0.42832783f32, -0.35213354, 0.53230917, 0.36544406]
            .iter().flat_map(|v| v.to_le_bytes()).map(|b| format!("{b:02x}"))
            .collect::<String>();
        let op = PatchOp {
            tensor: "t".into(), formula: "rank1_v1".into(),
            u_hex, cols: vec![1, 3, 4], alpha: "6.0".into(), dtype: "float32".into(),
        };
        let mut w = w0.to_vec();
        apply_rank1_f32(&mut w, 4, 6, &op);
        for (a, b) in w.iter().zip(expect.iter()) {
            assert!((a - b).abs() < 1e-5, "{a} vs {b}");
        }
        // unedited columns are bit-identical
        for r in 0..4 {
            for c in [0usize, 2, 5] {
                assert_eq!(w[r * 6 + c], w0[r * 6 + c]);
            }
        }
    }

    #[test]
    fn sha256_known_vector() {
        assert_eq!(
            sha256_hex(b"abc"),
            "ba7816bf8f01cfea414140de5dae2223b00361a396177a9cb410ff61f20015ad"
        );
    }
}
