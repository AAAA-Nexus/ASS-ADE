# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a2_mo_composites/mo_draft_testagentlooporchestrator.py:56
# Component id: sy.source.a2_mo_composites.test_orchestrator_on_step_end_called
from __future__ import annotations

__version__ = "0.1.0"

def test_orchestrator_on_step_end_called(self) -> None:
    o = MagicMock(spec=EngineOrchestrator)
    o.on_step_start.return_value = {}
    o.on_tool_event.return_value = []
    o.on_step_end.return_value = CycleReport(alerts=[])

    loop = self._make_loop(orchestrator=o)
    loop.step("Do something")
    o.on_step_end.assert_called_once()
