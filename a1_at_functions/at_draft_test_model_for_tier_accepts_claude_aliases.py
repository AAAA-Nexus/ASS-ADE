# Extracted from C:/!ass-ade/tests/test_free_providers.py:127
# Component id: at.source.ass_ade.test_model_for_tier_accepts_claude_aliases
from __future__ import annotations

__version__ = "0.1.0"

def test_model_for_tier_accepts_claude_aliases(self):
    p = get_provider("groq")
    assert p.model_for_tier("haiku") == p.models_by_tier["fast"]
    assert p.model_for_tier("sonnet") == p.models_by_tier["balanced"]
    assert p.model_for_tier("opus") == p.models_by_tier["deep"]
