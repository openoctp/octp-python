from octp.core.envelope import OCTPEnvelope, ProvenanceMethod, ReviewLevel


def test_envelope_parses_valid(valid_envelope_data):
    envelope = OCTPEnvelope.model_validate(valid_envelope_data)
    assert envelope.octp_version == "0.1"
    assert envelope.provenance.method == ProvenanceMethod.AI_ASSISTED_HUMAN_REVIEWED
    assert envelope.provenance.human_review_level == ReviewLevel.SUBSTANTIAL


def test_envelope_parses_minimal(minimal_envelope_data):
    envelope = OCTPEnvelope.model_validate(minimal_envelope_data)
    assert envelope.octp_version == "0.1"
    assert envelope.provenance.method == ProvenanceMethod.HUMAN_ONLY


def test_signable_dict_excludes_integrity(valid_envelope_data):
    envelope = OCTPEnvelope.model_validate(valid_envelope_data)
    signable = envelope.to_signable_dict()
    assert "integrity" not in signable


def test_envelope_requires_provenance():
    import pytest

    with pytest.raises(Exception):
        OCTPEnvelope.model_validate({"octp_version": "0.1"})
