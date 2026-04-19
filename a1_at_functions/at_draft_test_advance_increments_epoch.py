# Extracted from C:/!ass-ade/tests/test_session.py:30
# Component id: at.source.ass_ade.test_advance_increments_epoch
from __future__ import annotations

__version__ = "0.1.0"

def test_advance_increments_epoch(self) -> None:
    session = NexusSession(_mock_client())
    session.start("13608")
    session.advance()
    assert session.epoch == 1
