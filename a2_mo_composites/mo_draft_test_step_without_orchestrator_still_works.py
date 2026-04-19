# Extracted from C:/!ass-ade/.claude/worktrees/adoring-boyd-0e3a8f/tests/test_engine_integration.py:451
# Component id: mo.source.ass_ade.test_step_without_orchestrator_still_works
__version__ = "0.1.0"

    def test_step_without_orchestrator_still_works(self) -> None:
        loop = self._make_loop(orchestrator=None)
        result = loop.step("Hello")
        assert isinstance(result, str)
