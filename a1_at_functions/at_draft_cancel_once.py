# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a1_at_functions/at_draft_test_cancellation_context_is_thread_safe.py:16
# Component id: at.source.a1_at_functions.cancel_once
from __future__ import annotations

__version__ = "0.1.0"

def cancel_once():
    time.sleep(0.01)
    ctx.cancel()
