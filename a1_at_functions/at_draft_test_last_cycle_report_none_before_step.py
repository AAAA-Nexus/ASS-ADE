# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a1_at_functions/at_draft_test_last_cycle_report_none_before_step.py:7
# Component id: at.source.a1_at_functions.test_last_cycle_report_none_before_step
from __future__ import annotations

__version__ = "0.1.0"

def test_last_cycle_report_none_before_step(self) -> None:
    loop = self._make_loop()
    assert loop.last_cycle_report is None
