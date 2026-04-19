# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a2_mo_composites/mo_draft_test_fail_open_on_engine_error.py:7
# Component id: mo.source.a2_mo_composites.test_fail_open_on_engine_error
from __future__ import annotations

__version__ = "0.1.0"

def test_fail_open_on_engine_error(self) -> None:
    o = EngineOrchestrator({})
    # Corrupt the atlas to simulate failure
    o._atlas = MagicMock()
    o._atlas.decompose.side_effect = RuntimeError("engine crashed")
    o._atlas.complexity_score.side_effect = RuntimeError("engine crashed")
    # on_step_start should not raise
    result = o.on_step_start("task")
    assert isinstance(result, dict)
