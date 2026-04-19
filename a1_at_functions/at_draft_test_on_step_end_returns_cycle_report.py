# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a1_at_functions/at_draft_test_on_step_end_returns_cycle_report.py:7
# Component id: at.source.a1_at_functions.test_on_step_end_returns_cycle_report
from __future__ import annotations

__version__ = "0.1.0"

def test_on_step_end_returns_cycle_report(self) -> None:
    o = EngineOrchestrator({})
    o.on_step_start("do something")
    report = o.on_step_end("done", {"recon_done": True, "tool_calls": ["read_file"]})
    assert isinstance(report, CycleReport)
    assert isinstance(report.wisdom_score, float)
    assert isinstance(report.conviction, float)
    assert isinstance(report.alerts, list)
    assert isinstance(report.principles, list)
    assert isinstance(report.engine_reports, dict)
