# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a1_at_functions/at_draft_test_fail_open_on_internal_error.py:7
# Component id: at.source.a1_at_functions.test_fail_open_on_internal_error
from __future__ import annotations

__version__ = "0.1.0"

def test_fail_open_on_internal_error(self):
    lse = self._make({"lse": {"default_tier": "balanced"}})
    # Corrupt internal state — should still return a decision
    lse._trs_haiku_threshold = "not_a_float"  # type: ignore
    decision = lse.select(trs_score=0.9)
    assert decision.model is not None
