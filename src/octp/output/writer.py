from __future__ import annotations
import json
from pathlib import Path
from octp.core.envelope import OCTPEnvelope


def write_envelope(envelope: OCTPEnvelope, path: Path) -> None:
    """Write an envelope to disk as JSON."""
    path.write_text(envelope.model_dump_json(indent=2))


def write_envelope_string(envelope: OCTPEnvelope) -> str:
    """Return envelope as JSON string."""
    return envelope.model_dump_json(indent=2)
