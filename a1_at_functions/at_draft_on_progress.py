# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a1_at_functions/at_draft_test_callback_is_called.py:10
# Component id: at.source.a1_at_functions.on_progress
from __future__ import annotations

__version__ = "0.1.0"

def on_progress(name: str, status: StepStatus, current: int, total: int) -> None:
    calls.append((name, status, current, total))
