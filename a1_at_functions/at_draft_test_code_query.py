# Extracted from C:/!ass-ade/tests/test_routing.py:79
# Component id: at.source.ass_ade.test_code_query
from __future__ import annotations

__version__ = "0.1.0"

def test_code_query(self):
    decision = local_route("Write a function to parse JSON")
    assert decision.tier in (ModelTier.STANDARD, ModelTier.DEEP)
    assert decision.complexity >= 0.3
