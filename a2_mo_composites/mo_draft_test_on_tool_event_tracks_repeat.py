# Extracted from C:/!ass-ade/.claude/worktrees/beautiful-dubinsky-c2cb48/a2_mo_composites/mo_draft_testengineorchestrator.py:24
# Component id: mo.source.ass_ade.test_on_tool_event_tracks_repeat
__version__ = "0.1.0"

    def test_on_tool_event_tracks_repeat(self) -> None:
        o = EngineOrchestrator({})
        o.on_step_start("task")
        for _ in range(4):
            o.on_tool_event("read_file", {"path": "x"}, "ok")
        # After 4 repeats, loop_detected should fire
        # Check _step_tool_counts
        assert o._step_tool_counts.get("read_file", 0) == 4
