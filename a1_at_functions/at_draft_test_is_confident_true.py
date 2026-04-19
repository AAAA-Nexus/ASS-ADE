# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a1_at_functions/at_draft_test_is_confident_true.py:7
# Component id: at.source.a1_at_functions.test_is_confident_true
from __future__ import annotations

__version__ = "0.1.0"

def test_is_confident_true(self) -> None:
    w = WisdomEngine({"sde": {"conviction_required": 0.1}})
    # full state
    full = {f"q{i}": True for i in range(1, 51)}
    w.run_audit(full)
    assert w.is_confident
