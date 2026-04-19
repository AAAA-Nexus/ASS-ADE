# Extracted from C:/!ass-ade/tests/test_mcp_cancellation.py:35
# Component id: sy.source.ass_ade.test_cancellation_context_can_be_marked_cancelled
from __future__ import annotations

__version__ = "0.1.0"

def test_cancellation_context_can_be_marked_cancelled(self) -> None:
    ctx = CancellationContext()
    ctx.cancel()
    assert ctx.check() is True
    assert ctx.is_cancelled is True
