# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a1_at_functions/at_draft_test_policy_overrides_chain_order.py:7
# Component id: at.source.a1_at_functions.test_policy_overrides_chain_order
from __future__ import annotations

__version__ = "0.1.0"

def test_policy_overrides_chain_order(self, monkeypatch):
    monkeypatch.setenv("GROQ_API_KEY", "sk-a")
    monkeypatch.setenv("GEMINI_API_KEY", "sk-b")
    # Policy forces gemini for balanced
    match = select_provider_for_tier(
        "balanced",
        tier_policy={"balanced": "gemini"},
    )
    assert match is not None
    profile, _ = match
    assert profile.name == "gemini"
