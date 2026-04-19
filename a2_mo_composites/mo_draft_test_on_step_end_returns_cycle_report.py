# Extracted from C:/!ass-ade/.claude/worktrees/adoring-boyd-0e3a8f/tests/test_engine_integration.py:312
# Component id: mo.source.ass_ade.test_on_step_end_returns_cycle_report
__version__ = "0.1.0"

    def test_on_step_end_returns_cycle_report(self) -> None:
        o = EngineOrchestrator({})
        o.on_step_start("do something")
        report = o.on_step_end("done", {"recon_done": True, "tool_calls": ["read_file"]})
        assert isinstance(report, CycleReport)
        assert isinstance(report.wisdom_score, float)
        assert isinstance(report.conviction, float)
        assert isinstance(report.alerts, list)
        assert isinstance(report.principles, list)
        assert isinstance(report.engine_reports, dict)
