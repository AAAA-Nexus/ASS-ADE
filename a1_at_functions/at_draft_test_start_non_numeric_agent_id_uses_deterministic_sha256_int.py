# Extracted from C:/!ass-ade/tests/test_session.py:66
# Component id: at.source.ass_ade.test_start_non_numeric_agent_id_uses_deterministic_sha256_int
from __future__ import annotations

__version__ = "0.1.0"

def test_start_non_numeric_agent_id_uses_deterministic_sha256_int(self) -> None:
    client = _mock_client()
    session = NexusSession(client)

    agent_id = "agent-alpha"
    expected = int.from_bytes(
        hashlib.sha256(agent_id.encode("utf-8")).digest()[:4],
        "big",
    ) & 0x7FFFFFFF

    session.start(agent_id)
    session.start(agent_id)

    assert client.ratchet_register.call_count == 2
    first_arg = client.ratchet_register.call_args_list[0].args[0]
    second_arg = client.ratchet_register.call_args_list[1].args[0]
    assert first_arg == expected
    assert second_arg == expected
