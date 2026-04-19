# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a1_at_functions/at_draft_test_on_step_end_edee_traces.py:7
# Component id: at.source.a1_at_functions.test_on_step_end_edee_traces
from __future__ import annotations

__version__ = "0.1.0"

def test_on_step_end_edee_traces(self) -> None:
    o = EngineOrchestrator({})
    o.on_step_start("task")
    report = o.on_step_end("response", {})
    # EDEE should be initialized and have captured a trace
    assert o._edee is not None
    assert o.edee._traces >= 1
