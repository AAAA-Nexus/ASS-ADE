# Extracted from C:/!ass-ade/.claude/worktrees/adoring-boyd-0e3a8f/tests/test_engine_integration.py:368
# Component id: mo.source.ass_ade.test_fail_open_on_engine_error
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
