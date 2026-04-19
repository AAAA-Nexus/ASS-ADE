# Extracted from C:/!ass-ade/.claude/worktrees/beautiful-dubinsky-c2cb48/a2_mo_composites/mo_draft_testagentloopphase1.py:45
# Component id: at.source.ass_ade.test_refine_trigger_false_on_clean_report
__version__ = "0.1.0"

    def test_refine_trigger_false_on_clean_report(self):
        from ass_ade.agent.orchestrator import CycleReport
        loop = self._make_loop()
        report = CycleReport(alerts=[], wisdom_score=0.8)
        report.engine_reports["cie"] = {"patches_applied": 0}
        assert loop._check_refine_trigger(report) is False
