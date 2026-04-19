# Extracted from C:/!ass-ade/tests/test_free_providers.py:120
# Component id: at.source.ass_ade.test_model_for_tier_honors_override
from __future__ import annotations

__version__ = "0.1.0"

def test_model_for_tier_honors_override(self):
    p = get_provider("groq")
    override = {"fast": "my-custom-model"}
    assert p.model_for_tier("fast", override=override) == "my-custom-model"
    # Other tiers unaffected
    assert p.model_for_tier("deep", override=override) == p.models_by_tier["deep"]
