# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a2_mo_composites/mo_draft_testlseengine.py:45
# Component id: mo.source.a2_mo_composites.test_user_override_wins
from __future__ import annotations

__version__ = "0.1.0"

def test_user_override_wins(self):
    lse = self._make()
    decision = lse.select(trs_score=0.1, complexity="trivial", user_model_override="my-custom-model")
    assert decision.model == "my-custom-model"
    assert decision.reason == "user_override"
