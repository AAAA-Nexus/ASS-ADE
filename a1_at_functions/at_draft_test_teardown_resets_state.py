# Extracted from C:/!ass-ade/tests/test_session.py:58
# Component id: at.source.ass_ade.test_teardown_resets_state
from __future__ import annotations

__version__ = "0.1.0"

def test_teardown_resets_state(self) -> None:
    session = NexusSession(_mock_client())
    session.start("13608")
    session.teardown()
    assert not session.is_active
    assert session.session_id is None
    assert session.epoch == 0
