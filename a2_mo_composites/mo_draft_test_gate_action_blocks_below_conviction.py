# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a2_mo_composites/mo_draft_testwisdomengine.py:64
# Component id: mo.source.a2_mo_composites.test_gate_action_blocks_below_conviction
from __future__ import annotations

__version__ = "0.1.0"

def test_gate_action_blocks_below_conviction(self) -> None:
    w = WisdomEngine({})
    w.run_audit({})  # conviction → 0.25
    ok, reason = w.gate_action("deploy_to_prod", {})
    assert not ok
    assert "conviction" in reason
