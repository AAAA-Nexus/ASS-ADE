# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a1_at_functions/at_draft_test_start_creates_session.py:7
# Component id: at.source.a1_at_functions.test_start_creates_session
from __future__ import annotations

__version__ = "0.1.0"

def test_start_creates_session(self) -> None:
    session = NexusSession(_mock_client())
    result = session.start("13608")
    assert session.is_active
    assert session.session_id == "sess-abc"
    assert result.session_id == "sess-abc"
