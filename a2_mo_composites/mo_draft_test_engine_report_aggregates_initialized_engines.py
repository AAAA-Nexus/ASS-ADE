# Extracted from C:/!ass-ade/.claude/worktrees/adoring-boyd-0e3a8f/tests/test_engine_integration.py:360
# Component id: mo.source.ass_ade.test_engine_report_aggregates_initialized_engines
__version__ = "0.1.0"

    def test_engine_report_aggregates_initialized_engines(self) -> None:
        o = EngineOrchestrator({})
        _ = o.atlas  # initialize atlas
        _ = o.bas    # initialize bas
        reports = o.engine_report()
        assert "atlas" in reports
        assert "bas" in reports
