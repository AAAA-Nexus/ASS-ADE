# Extracted from C:/!ass-ade/.claude/worktrees/adoring-boyd-0e3a8f/tests/test_engine_integration.py:120
# Component id: mo.source.ass_ade.test_gate_action_allows_above_conviction
__version__ = "0.1.0"

    def test_gate_action_allows_above_conviction(self) -> None:
        w = WisdomEngine({"sde": {"conviction_required": 0.0}})
        ok, reason = w.gate_action("read_file", {})
        assert ok
        assert reason == "conviction_met"
