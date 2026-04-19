# Extracted from C:/!ass-ade/tests/test_routing.py:72
# Component id: mo.source.ass_ade.testlocalroute
from __future__ import annotations

__version__ = "0.1.0"

class TestLocalRoute:
    def test_simple_query(self):
        decision = local_route("What is 2 + 2?")
        assert decision.tier == ModelTier.FAST
        assert decision.source == "local"
        assert decision.recommended_model is not None

    def test_code_query(self):
        decision = local_route("Write a function to parse JSON")
        assert decision.tier in (ModelTier.STANDARD, ModelTier.DEEP)
        assert decision.complexity >= 0.3

    def test_decision_has_reason(self):
        decision = local_route("Hello")
        assert "heuristic" in decision.reason.lower()
