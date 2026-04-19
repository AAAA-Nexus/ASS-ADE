# Extracted from C:/!ass-ade/tests/test_session.py:41
# Component id: at.source.ass_ade.test_status_without_start_raises
from __future__ import annotations

__version__ = "0.1.0"

def test_status_without_start_raises(self) -> None:
    session = NexusSession(_mock_client())
    with pytest.raises(RuntimeError, match="No active session"):
        session.status()
