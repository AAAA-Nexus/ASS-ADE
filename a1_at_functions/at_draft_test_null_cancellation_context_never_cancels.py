# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a1_at_functions/at_draft_test_null_cancellation_context_never_cancels.py:7
# Component id: at.source.a1_at_functions.test_null_cancellation_context_never_cancels
from __future__ import annotations

__version__ = "0.1.0"

def test_null_cancellation_context_never_cancels(self) -> None:
    ctx = NullCancellationContext()
    ctx.cancel()
    assert ctx.check() is False
    assert ctx.is_cancelled is False
