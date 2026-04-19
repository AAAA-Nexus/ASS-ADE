# Extracted from C:/!ass-ade/tests/test_session.py:36
# Component id: at.source.ass_ade.test_advance_without_start_raises
from __future__ import annotations

__version__ = "0.1.0"

def test_advance_without_start_raises(self) -> None:
    session = NexusSession(_mock_client())
    with pytest.raises(RuntimeError, match="No active session"):
        session.advance()
