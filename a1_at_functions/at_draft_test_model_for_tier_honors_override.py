# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a1_at_functions/at_draft_test_model_for_tier_honors_override.py:7
# Component id: at.source.a1_at_functions.test_model_for_tier_honors_override
from __future__ import annotations

__version__ = "0.1.0"

def test_model_for_tier_honors_override(self):
    p = get_provider("groq")
    override = {"fast": "my-custom-model"}
    assert p.model_for_tier("fast", override=override) == "my-custom-model"
    # Other tiers unaffected
    assert p.model_for_tier("deep", override=override) == p.models_by_tier["deep"]
