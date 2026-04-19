# Extracted from C:/!ass-ade/tests/test_engine_integration.py:351
# Component id: mo.source.ass_ade.test_step_metrics_reset_on_start
from __future__ import annotations

__version__ = "0.1.0"

def test_step_metrics_reset_on_start(self) -> None:
    o = EngineOrchestrator({})
    o.on_step_start("first task")
    o.on_tool_event("read_file", {}, "")
    assert o._step_tool_counts.get("read_file", 0) == 1
    # Second step start should reset
    o.on_step_start("second task")
    assert o._step_tool_counts == {}
