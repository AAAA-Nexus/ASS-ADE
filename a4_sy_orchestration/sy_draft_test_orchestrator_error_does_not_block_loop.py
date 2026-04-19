# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a2_mo_composites/mo_draft_testagentlooporchestrator.py:66
# Component id: sy.source.a2_mo_composites.test_orchestrator_error_does_not_block_loop
from __future__ import annotations

__version__ = "0.1.0"

def test_orchestrator_error_does_not_block_loop(self) -> None:
    o = MagicMock(spec=EngineOrchestrator)
    o.on_step_start.side_effect = RuntimeError("engine down")
    o.on_tool_event.side_effect = RuntimeError("engine down")
    o.on_step_end.side_effect = RuntimeError("engine down")

    loop = self._make_loop(orchestrator=o)
    # Should not raise — fail-open design
    result = loop.step("Do something")
    assert isinstance(result, str)
