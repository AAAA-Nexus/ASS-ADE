# Extracted from C:/!ass-ade/tests/test_engine_integration.py:444
# Component id: mo.source.ass_ade.test_last_cycle_report_set_after_step
from __future__ import annotations

__version__ = "0.1.0"

def test_last_cycle_report_set_after_step(self) -> None:
    o = EngineOrchestrator({})
    loop = self._make_loop(orchestrator=o)
    loop.step("Write hello world")
    assert loop.last_cycle_report is not None
    assert isinstance(loop.last_cycle_report, CycleReport)
