# Extracted from C:/!ass-ade/tests/test_session.py:23
# Component id: at.source.ass_ade.test_start_creates_session
from __future__ import annotations

__version__ = "0.1.0"

def test_start_creates_session(self) -> None:
    session = NexusSession(_mock_client())
    result = session.start("13608")
    assert session.is_active
    assert session.session_id == "sess-abc"
    assert result.session_id == "sess-abc"
