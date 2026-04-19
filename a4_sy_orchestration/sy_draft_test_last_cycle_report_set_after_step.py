# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a2_mo_composites/mo_draft_testagentlooporchestrator.py:34
# Component id: sy.source.a2_mo_composites.test_last_cycle_report_set_after_step
from __future__ import annotations

__version__ = "0.1.0"

def test_last_cycle_report_set_after_step(self) -> None:
    o = EngineOrchestrator({})
    loop = self._make_loop(orchestrator=o)
    loop.step("Write hello world")
    assert loop.last_cycle_report is not None
    assert isinstance(loop.last_cycle_report, CycleReport)
