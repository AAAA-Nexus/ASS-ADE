# Extracted from C:/!ass-ade/tests/test_free_providers.py:209
# Component id: at.source.ass_ade.test_falls_through_when_policy_unavailable
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
