# Extracted from C:/!ass-ade/.claude/worktrees/adoring-boyd-0e3a8f/tests/test_engine_integration.py:113
# Component id: mo.source.ass_ade.test_gate_action_blocks_below_conviction
__version__ = "0.1.0"

    def test_gate_action_blocks_below_conviction(self) -> None:
        w = WisdomEngine({})
        w.run_audit({})  # conviction → 0.25
        ok, reason = w.gate_action("deploy_to_prod", {})
        assert not ok
        assert "conviction" in reason
