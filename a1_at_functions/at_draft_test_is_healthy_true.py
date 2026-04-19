# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a1_at_functions/at_draft_test_is_healthy_true.py:7
# Component id: at.source.a1_at_functions.test_is_healthy_true
from __future__ import annotations

__version__ = "0.1.0"

def test_is_healthy_true(self) -> None:
    session = NexusSession(_mock_client())
    session.start("13608")
    assert session.is_healthy()
