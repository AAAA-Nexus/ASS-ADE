# Extracted from C:/!ass-ade/.claude/worktrees/adoring-boyd-0e3a8f/tests/test_phase_engines.py:384
# Component id: mo.source.ass_ade.test_report_tracks_passes_failures
__version__ = "0.1.0"

    def test_report_tracks_passes_failures(self):
        from ass_ade.agent.cie import CIEPipeline
        cie = CIEPipeline({"cie": {"enable_lint": False}})
        cie.run("x = 1\n", "python")
        cie.run("def bad(:\n    pass\n", "python")
        rep = cie.report()
        assert rep["passes"] >= 1
        assert rep["failures"] >= 1
        assert 0.0 <= rep["pass_rate"] <= 1.0
