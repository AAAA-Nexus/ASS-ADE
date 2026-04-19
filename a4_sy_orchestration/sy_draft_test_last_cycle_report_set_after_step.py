# Extracted from C:/!ass-ade/.claude/worktrees/beautiful-dubinsky-c2cb48/a2_mo_composites/mo_draft_testagentlooporchestrator.py:32
# Component id: sy.source.ass_ade.test_last_cycle_report_set_after_step
__version__ = "0.1.0"

    def test_last_cycle_report_set_after_step(self) -> None:
        o = EngineOrchestrator({})
        loop = self._make_loop(orchestrator=o)
        loop.step("Write hello world")
        assert loop.last_cycle_report is not None
        assert isinstance(loop.last_cycle_report, CycleReport)
