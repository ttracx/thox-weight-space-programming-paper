//! CLI: thox-patch-loader <verify|apply|rollback|status>
//!
//! verify  --manifest m.json --pubkey pub.bin
//! apply   --manifest m.json --pubkey pub.bin --store DIR --shapes shapes.json
//! rollback --store DIR
//! status  --store DIR
use std::collections::BTreeMap;
use std::path::Path;
use thox_patch_loader::{verify_signature, SlotStore};

fn arg(args: &[String], name: &str) -> Result<String, String> {
    args.windows(2)
        .find(|w| w[0] == name)
        .map(|w| w[1].clone())
        .ok_or_else(|| format!("missing {name}"))
}

fn main() {
    let args: Vec<String> = std::env::args().collect();
    let cmd = args.get(1).map(|s| s.as_str()).unwrap_or("");
    let run = || -> Result<String, String> {
        match cmd {
            "verify" | "apply" => {
                let manifest = std::fs::read_to_string(arg(&args, "--manifest")?)
                    .map_err(|e| e.to_string())?;
                let pub_bytes = std::fs::read(arg(&args, "--pubkey")?).map_err(|e| e.to_string())?;
                let mut pk = [0u8; 32];
                if pub_bytes.len() != 32 { return Err("pubkey must be 32 raw bytes".into()); }
                pk.copy_from_slice(&pub_bytes);
                let m = verify_signature(&manifest, &pk)?;
                if cmd == "verify" {
                    return Ok(format!("signature OK; {} ops; base {} @ {}",
                                      m.ops.len(), m.base_repo, m.base_revision));
                }
                let store = SlotStore::open(Path::new(&arg(&args, "--store")?));
                let shapes_txt = std::fs::read_to_string(arg(&args, "--shapes")?)
                    .map_err(|e| e.to_string())?;
                let shapes: BTreeMap<String, (usize, usize)> =
                    serde_json::from_str(&shapes_txt).map_err(|e| e.to_string())?;
                let slot = store.apply(&m, &shapes)?;
                Ok(format!("patch applied and verified; active slot is now {slot}"))
            }
            "rollback" => {
                let store = SlotStore::open(Path::new(&arg(&args, "--store")?));
                let slot = store.rollback()?;
                Ok(format!("rolled back; active slot is now {slot}"))
            }
            "status" => {
                let store = SlotStore::open(Path::new(&arg(&args, "--store")?));
                Ok(format!("active slot: {}", store.active_slot()))
            }
            _ => Err("usage: thox-patch-loader <verify|apply|rollback|status> [flags]".into()),
        }
    };
    match run() {
        Ok(msg) => println!("{msg}"),
        Err(e) => { eprintln!("ERROR: {e}"); std::process::exit(1); }
    }
}
