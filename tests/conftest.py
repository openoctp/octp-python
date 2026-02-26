import json
from pathlib import Path

import pytest

FIXTURES_DIR = Path(__file__).parent / "fixtures"


@pytest.fixture
def valid_envelope_data():
    return json.loads((FIXTURES_DIR / "valid_envelope.json").read_text())


@pytest.fixture
def minimal_envelope_data():
    return json.loads((FIXTURES_DIR / "minimal_envelope.json").read_text())
