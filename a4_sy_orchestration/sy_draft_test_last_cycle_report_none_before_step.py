# Extracted from C:/!ass-ade/.claude/worktrees/beautiful-dubinsky-c2cb48/a2_mo_composites/mo_draft_testagentlooporchestrator.py:28
# Component id: sy.source.ass_ade.test_last_cycle_report_none_before_step
__version__ = "0.1.0"

    def test_last_cycle_report_none_before_step(self) -> None:
        loop = self._make_loop()
        assert loop.last_cycle_report is None
