# Extracted from C:/!ass-ade/tests/test_engine_integration.py:343
# Component id: mo.source.ass_ade.test_on_step_end_edee_traces
from __future__ import annotations

__version__ = "0.1.0"

def test_on_step_end_edee_traces(self) -> None:
    o = EngineOrchestrator({})
    o.on_step_start("task")
    report = o.on_step_end("response", {})
    # EDEE should be initialized and have captured a trace
    assert o._edee is not None
    assert o.edee._traces >= 1
