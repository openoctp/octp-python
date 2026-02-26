from __future__ import annotations
import base64
from pathlib import Path
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives.asymmetric.utils import (
    decode_dss_signature,
    encode_dss_signature,
)


KEYS_DIR = Path.home() / ".octp" / "keys"
PRIVATE_KEY_FILE = KEYS_DIR / "private.pem"
PUBLIC_KEY_FILE = KEYS_DIR / "public.pem"


def ensure_keypair() -> None:
    """Generate keypair if it doesn't exist."""
    if PRIVATE_KEY_FILE.exists():
        return
    KEYS_DIR.mkdir(parents=True, exist_ok=True)
    private_key = ec.generate_private_key(ec.SECP256R1())
    public_key = private_key.public_key()

    with open(PRIVATE_KEY_FILE, "wb") as f:
        f.write(
            private_key.private_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PrivateFormat.PKCS8,
                encryption_algorithm=serialization.NoEncryption(),
            )
        )
    PRIVATE_KEY_FILE.chmod(0o600)

    with open(PUBLIC_KEY_FILE, "wb") as f:
        f.write(
            public_key.public_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PublicFormat.SubjectPublicKeyInfo,
            )
        )


def sign_payload(payload_hash: str) -> str:
    """Sign a payload hash with the developer's private key.
    Returns base64-encoded signature."""
    ensure_keypair()
    with open(PRIVATE_KEY_FILE, "rb") as f:
        private_key = serialization.load_pem_private_key(f.read(), password=None)

    signature = private_key.sign(
        payload_hash.encode(),
        ec.ECDSA(hashes.SHA256()),
    )
    return base64.b64encode(signature).decode()


def get_public_key_pem() -> str:
    """Return the developer's public key in PEM format."""
    ensure_keypair()
    return PUBLIC_KEY_FILE.read_text()


def verify_signature(
    payload_hash: str, signature_b64: str, public_key_pem: str
) -> bool:
    """Verify a signature against a payload hash and public key."""
    try:
        public_key = serialization.load_pem_public_key(public_key_pem.encode())
        signature = base64.b64decode(signature_b64)
        public_key.verify(
            signature,
            payload_hash.encode(),
            ec.ECDSA(hashes.SHA256()),
        )
        return True
    except Exception:
        return False
