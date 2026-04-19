# Extracted from C:/!ass-ade/tests/test_routing.py:84
# Component id: at.source.ass_ade.test_decision_has_reason
from __future__ import annotations

__version__ = "0.1.0"

def test_decision_has_reason(self):
    decision = local_route("Hello")
    assert "heuristic" in decision.reason.lower()
