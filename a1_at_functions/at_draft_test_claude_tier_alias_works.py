# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a1_at_functions/at_draft_test_claude_tier_alias_works.py:7
# Component id: at.source.a1_at_functions.test_claude_tier_alias_works
from __future__ import annotations

__version__ = "0.1.0"

def test_claude_tier_alias_works(self, monkeypatch):
    monkeypatch.setenv("GROQ_API_KEY", "sk-a")
    match = select_provider_for_tier("haiku")  # alias for "fast"
    assert match is not None
    profile, model = match
    assert model == profile.models_by_tier["fast"]
