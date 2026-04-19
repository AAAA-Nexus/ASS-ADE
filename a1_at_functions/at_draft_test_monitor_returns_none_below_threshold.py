# Extracted from C:/!ass-ade/.claude/worktrees/beautiful-dubinsky-c2cb48/a2_mo_composites/mo_draft_testbas.py:13
# Component id: at.source.ass_ade.test_monitor_returns_none_below_threshold
__version__ = "0.1.0"

    def test_monitor_returns_none_below_threshold(self) -> None:
        b = BAS({})
        a = b.monitor({"synergy": 0.1, "novelty": 0.1, "gvu_delta": 0.0})
        assert a is None
