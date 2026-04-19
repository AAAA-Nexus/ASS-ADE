# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a1_at_functions/at_draft_test_lse_user_override_bypasses_catalog.py:7
# Component id: at.source.a1_at_functions.test_lse_user_override_bypasses_catalog
from __future__ import annotations

__version__ = "0.1.0"

def test_lse_user_override_bypasses_catalog(self):
    from ass_ade.agent.lse import LSEEngine
    lse = LSEEngine({})
    decision = lse.select(
        trs_score=0.8, complexity="medium", user_model_override="my-fixed-model",
    )
    assert decision.model == "my-fixed-model"
    assert decision.provider is None
    assert decision.reason == "user_override"
