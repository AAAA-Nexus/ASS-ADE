# Extracted from C:/!ass-ade/.claude/worktrees/beautiful-dubinsky-c2cb48/a2_mo_composites/mo_draft_testagentloopphase1.py:41
# Component id: at.source.ass_ade.test_refine_trigger_false_when_no_report
__version__ = "0.1.0"

    def test_refine_trigger_false_when_no_report(self):
        loop = self._make_loop()
        assert loop._check_refine_trigger(None) is False
