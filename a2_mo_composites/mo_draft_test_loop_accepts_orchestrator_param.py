# Extracted from C:/!ass-ade/.claude/worktrees/adoring-boyd-0e3a8f/tests/test_engine_integration.py:435
# Component id: mo.source.ass_ade.test_loop_accepts_orchestrator_param
__version__ = "0.1.0"

    def test_loop_accepts_orchestrator_param(self) -> None:
        o = EngineOrchestrator({})
        loop = self._make_loop(orchestrator=o)
        assert loop._orchestrator is o
