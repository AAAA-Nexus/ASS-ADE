# Extracted from C:/!ass-ade/.claude/worktrees/adoring-boyd-0e3a8f/tests/test_engine_integration.py:180
# Component id: mo.source.ass_ade.test_monitor_returns_none_below_threshold
__version__ = "0.1.0"

    def test_monitor_returns_none_below_threshold(self) -> None:
        b = BAS({})
        a = b.monitor({"synergy": 0.1, "novelty": 0.1, "gvu_delta": 0.0})
        assert a is None
