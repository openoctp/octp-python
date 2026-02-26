from __future__ import annotations
import json
from pathlib import Path
from octp.core.envelope import OCTPEnvelope


def validate_envelope_json(data: dict) -> bool:
    """Validate that a dict conforms to OCTP v0.1 envelope schema."""
    try:
        envelope = OCTPEnvelope.model_validate(data)
        return True
    except Exception:
        return False


def validate_envelope_file(path: Path) -> tuple[bool, str]:
    """Validate an envelope file.
    Returns (is_valid, error_message)."""
    try:
        data = json.loads(path.read_text())
        OCTPEnvelope.model_validate(data)
        return True, ""
    except json.JSONDecodeError as e:
        return False, f"Invalid JSON: {e}"
    except Exception as e:
        return False, f"Schema validation failed: {e}"
