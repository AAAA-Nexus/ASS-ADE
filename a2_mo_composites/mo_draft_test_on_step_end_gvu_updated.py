# Extracted from C:/!ass-ade/.claude/worktrees/adoring-boyd-0e3a8f/tests/test_engine_integration.py:337
# Component id: mo.source.ass_ade.test_on_step_end_gvu_updated
__version__ = "0.1.0"

    def test_on_step_end_gvu_updated(self) -> None:
        o = EngineOrchestrator({})
        o.on_step_start("task")
        report = o.on_step_end("response", {})
        assert report.gvu_coefficient > 0.0
