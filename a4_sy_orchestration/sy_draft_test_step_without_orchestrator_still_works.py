# Extracted from C:/!ass-ade/.claude/worktrees/beautiful-dubinsky-c2cb48/a2_mo_composites/mo_draft_testagentlooporchestrator.py:39
# Component id: sy.source.ass_ade.test_step_without_orchestrator_still_works
__version__ = "0.1.0"

    def test_step_without_orchestrator_still_works(self) -> None:
        loop = self._make_loop(orchestrator=None)
        result = loop.step("Hello")
        assert isinstance(result, str)
