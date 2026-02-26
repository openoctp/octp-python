from octp.integrity.hasher import hash_payload


def test_hash_is_deterministic():
    data = {"key": "value", "number": 42}
    assert hash_payload(data) == hash_payload(data)


def test_hash_changes_with_data():
    data1 = {"key": "value1"}
    data2 = {"key": "value2"}
    assert hash_payload(data1) != hash_payload(data2)


def test_hash_is_hex_string():
    result = hash_payload({"test": True})
    assert len(result) == 64
    assert all(c in "0123456789abcdef" for c in result)
