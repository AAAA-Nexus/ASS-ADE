# Extracted from C:/!ass-ade/.claude/worktrees/adoring-boyd-0e3a8f/tests/test_engine_integration.py:126
# Component id: mo.source.ass_ade.test_distill_principles_from_failures
__version__ = "0.1.0"

    def test_distill_principles_from_failures(self) -> None:
        w = WisdomEngine({})
        report = w.run_audit({})  # all failed
        principles = w.distill_principles(report)
        assert isinstance(principles, list)
        assert len(principles) >= 1
        assert all(isinstance(p, str) and p for p in principles)
