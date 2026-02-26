from __future__ import annotations
import hashlib
import json


def hash_payload(data: dict) -> str:
    """Compute SHA-256 hash of envelope payload.

    Data is serialised to JSON with sorted keys for determinism.
    Returns lowercase hex string.
    """
    serialised = json.dumps(data, sort_keys=True, ensure_ascii=True)
    return hashlib.sha256(serialised.encode()).hexdigest()
