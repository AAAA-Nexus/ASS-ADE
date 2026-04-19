# Extracted from C:/!ass-ade/.claude/worktrees/adoring-boyd-0e3a8f/tests/test_engine_integration.py:323
# Component id: mo.source.ass_ade.test_on_step_end_wisdom_scores
__version__ = "0.1.0"

    def test_on_step_end_wisdom_scores(self) -> None:
        o = EngineOrchestrator({})
        o.on_step_start("task")
        report = o.on_step_end("response", {
            "recon_done": True,
            "atlas_used": True,
            "lifr_queried": True,
            "memory_consulted": True,
            "budget_ok": True,
            "tool_calls": ["read_file"],
        })
        assert report.wisdom_score > 0.0
        assert report.wisdom_passed > 0
