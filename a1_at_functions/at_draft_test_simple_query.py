# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a1_at_functions/at_draft_test_simple_query.py:7
# Component id: at.source.a1_at_functions.test_simple_query
from __future__ import annotations

__version__ = "0.1.0"

def test_simple_query(self):
    decision = local_route("What is 2 + 2?")
    assert decision.tier == ModelTier.FAST
    assert decision.source == "local"
    assert decision.recommended_model is not None
