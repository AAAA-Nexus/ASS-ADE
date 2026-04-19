# Extracted from C:/!ass-ade/tests/test_phase_engines.py:55
# Component id: mo.source.ass_ade.test_user_override_wins
from __future__ import annotations

__version__ = "0.1.0"

def test_user_override_wins(self):
    lse = self._make()
    decision = lse.select(trs_score=0.1, complexity="trivial", user_model_override="my-custom-model")
    assert decision.model == "my-custom-model"
    assert decision.reason == "user_override"
