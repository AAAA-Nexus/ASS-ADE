# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a1_at_functions/at_draft_test_refine_trigger_false_on_clean_report.py:7
# Component id: at.source.a1_at_functions.test_refine_trigger_false_on_clean_report
from __future__ import annotations

__version__ = "0.1.0"

def test_refine_trigger_false_on_clean_report(self):
    from ass_ade.agent.orchestrator import CycleReport
    loop = self._make_loop()
    report = CycleReport(alerts=[], wisdom_score=0.8)
    report.engine_reports["cie"] = {"patches_applied": 0}
    assert loop._check_refine_trigger(report) is False
