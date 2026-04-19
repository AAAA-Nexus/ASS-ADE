# Extracted from C:/!ass-ade/tests/test_session.py:46
# Component id: at.source.ass_ade.test_is_healthy_true
from __future__ import annotations

__version__ = "0.1.0"

def test_is_healthy_true(self) -> None:
    session = NexusSession(_mock_client())
    session.start("13608")
    assert session.is_healthy()
