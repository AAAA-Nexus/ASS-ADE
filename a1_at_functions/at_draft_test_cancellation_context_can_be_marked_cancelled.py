# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a1_at_functions/at_draft_test_cancellation_context_can_be_marked_cancelled.py:7
# Component id: at.source.a1_at_functions.test_cancellation_context_can_be_marked_cancelled
from __future__ import annotations

__version__ = "0.1.0"

def test_cancellation_context_can_be_marked_cancelled(self) -> None:
    ctx = CancellationContext()
    ctx.cancel()
    assert ctx.check() is True
    assert ctx.is_cancelled is True
