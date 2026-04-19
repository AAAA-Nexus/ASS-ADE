# Extracted from C:/!ass-ade/.claude/worktrees/beautiful-dubinsky-c2cb48/a2_mo_composites/mo_draft_testagentlooporchestrator.py:23
# Component id: sy.source.ass_ade.test_loop_accepts_orchestrator_param
__version__ = "0.1.0"

    def test_loop_accepts_orchestrator_param(self) -> None:
        o = EngineOrchestrator({})
        loop = self._make_loop(orchestrator=o)
        assert loop._orchestrator is o
