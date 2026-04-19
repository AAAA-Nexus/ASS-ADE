# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a2_mo_composites/mo_draft_testengineorchestrator.py:26
# Component id: mo.source.a2_mo_composites.test_on_tool_event_tracks_repeat
from __future__ import annotations

__version__ = "0.1.0"

def test_on_tool_event_tracks_repeat(self) -> None:
    o = EngineOrchestrator({})
    o.on_step_start("task")
    for _ in range(4):
        o.on_tool_event("read_file", {"path": "x"}, "ok")
    # After 4 repeats, loop_detected should fire
    # Check _step_tool_counts
    assert o._step_tool_counts.get("read_file", 0) == 4
