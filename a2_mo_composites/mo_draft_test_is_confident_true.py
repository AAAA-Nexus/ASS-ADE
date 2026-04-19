# Extracted from C:/!ass-ade/tests/test_engine_integration.py:99
# Component id: mo.source.ass_ade.test_is_confident_true
from __future__ import annotations

__version__ = "0.1.0"

def test_is_confident_true(self) -> None:
    w = WisdomEngine({"sde": {"conviction_required": 0.1}})
    # full state
    full = {f"q{i}": True for i in range(1, 51)}
    w.run_audit(full)
    assert w.is_confident
