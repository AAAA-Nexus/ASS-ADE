# Extracted from C:/!ass-ade/.claude/worktrees/adoring-boyd-0e3a8f/tests/test_engine_integration.py:456
# Component id: mo.source.ass_ade.test_orchestrator_on_step_start_called
__version__ = "0.1.0"

    def test_orchestrator_on_step_start_called(self) -> None:
        o = MagicMock(spec=EngineOrchestrator)
        o.on_step_start.return_value = {}
        o.on_tool_event.return_value = []
        o.on_step_end.return_value = CycleReport(alerts=[])

        loop = self._make_loop(orchestrator=o)
        loop.step("Do something")
        o.on_step_start.assert_called_once()
