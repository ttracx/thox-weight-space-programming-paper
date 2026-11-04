"""Ed25519 signing for patch manifests.

The release key lives OUTSIDE the editing environment (whitepaper
lifecycle step 5). Devices and loaders verify with the public key.
"""
from cryptography.hazmat.primitives.asymmetric.ed25519 import (
    Ed25519PrivateKey, Ed25519PublicKey)
from cryptography.hazmat.primitives import serialization
from .manifest import Manifest

def generate_keypair() -> tuple[bytes, bytes]:
    k = Ed25519PrivateKey.generate()
    priv = k.private_bytes(serialization.Encoding.Raw,
                           serialization.PrivateFormat.Raw,
                           serialization.NoEncryption())
    pub = k.public_key().public_bytes(serialization.Encoding.Raw,
                                      serialization.PublicFormat.Raw)
    return priv, pub

def sign_manifest(m: Manifest, priv_raw: bytes) -> Manifest:
    k = Ed25519PrivateKey.from_private_bytes(priv_raw)
    m.signature = k.sign(m.canonical_bytes()).hex()
    return m

def verify_manifest(m: Manifest, pub_raw: bytes) -> bool:
    try:
        Ed25519PublicKey.from_public_bytes(pub_raw).verify(
            bytes.fromhex(m.signature), m.canonical_bytes())
        return True
    except Exception:
        return False
