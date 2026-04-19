# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a1_at_functions/at_draft_test_falls_through_when_policy_unavailable.py:7
# Component id: at.source.a1_at_functions.test_falls_through_when_policy_unavailable
from __future__ import annotations

__version__ = "0.1.0"

def test_falls_through_when_policy_unavailable(self, monkeypatch):
    # Policy says gemini, but gemini has no key — fall through to next chain provider
    for p in FREE_PROVIDERS.values():
        if p.api_key_env:
            monkeypatch.delenv(p.api_key_env, raising=False)
    monkeypatch.setenv("GROQ_API_KEY", "sk-a")
    match = select_provider_for_tier(
        "balanced",
        tier_policy={"balanced": "gemini"},
    )
    assert match is not None
    profile, _ = match
    # Falls through to groq (only one with a key)
    assert profile.name == "groq"
