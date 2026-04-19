# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a1_at_functions/at_draft_test_advance_increments_epoch.py:7
# Component id: at.source.a1_at_functions.test_advance_increments_epoch
from __future__ import annotations

__version__ = "0.1.0"

def test_advance_increments_epoch(self) -> None:
    session = NexusSession(_mock_client())
    session.start("13608")
    session.advance()
    assert session.epoch == 1
