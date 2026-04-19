# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a1_at_functions/at_draft_test_model_for_tier_accepts_claude_aliases.py:7
# Component id: at.source.a1_at_functions.test_model_for_tier_accepts_claude_aliases
from __future__ import annotations

__version__ = "0.1.0"

def test_model_for_tier_accepts_claude_aliases(self):
    p = get_provider("groq")
    assert p.model_for_tier("haiku") == p.models_by_tier["fast"]
    assert p.model_for_tier("sonnet") == p.models_by_tier["balanced"]
    assert p.model_for_tier("opus") == p.models_by_tier["deep"]
