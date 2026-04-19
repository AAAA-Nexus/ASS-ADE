# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a1_at_functions/at_draft_test_concurrent_cancellation_scenario.py:16
# Component id: at.source.a1_at_functions.delayed_cancel
from __future__ import annotations

__version__ = "0.1.0"

def delayed_cancel():
    time.sleep(0.05)
    ctx.cancel()
