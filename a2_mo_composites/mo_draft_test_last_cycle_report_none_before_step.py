# Extracted from C:/!ass-ade/.claude/worktrees/adoring-boyd-0e3a8f/tests/test_engine_integration.py:440
# Component id: mo.source.ass_ade.test_last_cycle_report_none_before_step
__version__ = "0.1.0"

    def test_last_cycle_report_none_before_step(self) -> None:
        loop = self._make_loop()
        assert loop.last_cycle_report is None
