# Extracted from C:/!ass-ade/tests/test_routing.py:73
# Component id: at.source.ass_ade.test_simple_query
from __future__ import annotations

__version__ = "0.1.0"

def test_simple_query(self):
    decision = local_route("What is 2 + 2?")
    assert decision.tier == ModelTier.FAST
    assert decision.source == "local"
    assert decision.recommended_model is not None
