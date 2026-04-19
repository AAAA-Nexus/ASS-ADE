# Extracted from C:/!ass-ade/tests/test_session.py:51
# Component id: at.source.ass_ade.test_is_healthy_false_when_no_calls
from __future__ import annotations

__version__ = "0.1.0"

def test_is_healthy_false_when_no_calls(self) -> None:
    client = _mock_client()
    client.ratchet_status.return_value = RatchetStatus(remaining_calls=0)
    session = NexusSession(client)
    session.start("13608")
    assert not session.is_healthy()
