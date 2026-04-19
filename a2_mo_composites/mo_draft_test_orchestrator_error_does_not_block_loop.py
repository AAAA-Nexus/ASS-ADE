# Extracted from C:/!ass-ade/.claude/worktrees/adoring-boyd-0e3a8f/tests/test_engine_integration.py:476
# Component id: mo.source.ass_ade.test_orchestrator_error_does_not_block_loop
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
