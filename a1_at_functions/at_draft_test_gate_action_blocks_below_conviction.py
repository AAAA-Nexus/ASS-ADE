# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a1_at_functions/at_draft_test_gate_action_blocks_below_conviction.py:7
# Component id: at.source.a1_at_functions.test_gate_action_blocks_below_conviction
from __future__ import annotations

__version__ = "0.1.0"

def test_gate_action_blocks_below_conviction(self) -> None:
    w = WisdomEngine({})
    w.run_audit({})  # conviction → 0.25
    ok, reason = w.gate_action("deploy_to_prod", {})
    assert not ok
    assert "conviction" in reason
