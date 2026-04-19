# Extracted from C:/!ass-ade/.claude/worktrees/adoring-boyd-0e3a8f/tests/test_engine_integration.py:225
# Component id: mo.source.ass_ade.test_subscriber_exception_does_not_propagate
__version__ = "0.1.0"

    def test_subscriber_exception_does_not_propagate(self) -> None:
        b = BAS({})
        b.subscribe(lambda a: (_ for _ in ()).throw(RuntimeError("boom")))
        # Should not raise
        b.monitor_all({"synergy": 0.9})
