# Extracted from C:/!ass-ade/tests/test_phase_engines.py:143
# Component id: mo.source.ass_ade.test_refine_trigger_false_on_clean_report
from __future__ import annotations

__version__ = "0.1.0"

def test_refine_trigger_false_on_clean_report(self):
    from ass_ade.agent.orchestrator import CycleReport
    loop = self._make_loop()
    report = CycleReport(alerts=[], wisdom_score=0.8)
    report.engine_reports["cie"] = {"patches_applied": 0}
    assert loop._check_refine_trigger(report) is False
