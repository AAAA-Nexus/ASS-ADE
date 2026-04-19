# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a1_at_functions/at_draft_test_gate_action_allows_above_conviction.py:7
# Component id: at.source.a1_at_functions.test_gate_action_allows_above_conviction
from __future__ import annotations

__version__ = "0.1.0"

def test_gate_action_allows_above_conviction(self) -> None:
    w = WisdomEngine({"sde": {"conviction_required": 0.0}})
    ok, reason = w.gate_action("read_file", {})
    assert ok
    assert reason == "conviction_met"
