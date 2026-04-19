# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a1_at_functions/at_draft_test_refine_trigger_false_when_no_report.py:7
# Component id: at.source.a1_at_functions.test_refine_trigger_false_when_no_report
from __future__ import annotations

__version__ = "0.1.0"

def test_refine_trigger_false_when_no_report(self):
    loop = self._make_loop()
    assert loop._check_refine_trigger(None) is False
