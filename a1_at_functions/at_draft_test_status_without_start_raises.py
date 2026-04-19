# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a1_at_functions/at_draft_test_status_without_start_raises.py:7
# Component id: at.source.a1_at_functions.test_status_without_start_raises
from __future__ import annotations

__version__ = "0.1.0"

def test_status_without_start_raises(self) -> None:
    session = NexusSession(_mock_client())
    with pytest.raises(RuntimeError, match="No active session"):
        session.status()
