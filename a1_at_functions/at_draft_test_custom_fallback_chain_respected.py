# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a1_at_functions/at_draft_test_custom_fallback_chain_respected.py:7
# Component id: at.source.a1_at_functions.test_custom_fallback_chain_respected
from __future__ import annotations

__version__ = "0.1.0"

def test_custom_fallback_chain_respected(self, monkeypatch):
    monkeypatch.setenv("GROQ_API_KEY", "sk-a")
    monkeypatch.setenv("GEMINI_API_KEY", "sk-b")
    # Custom chain puts gemini first
    match = select_provider_for_tier(
        "balanced",
        fallback_chain=["gemini", "groq"],
    )
    assert match is not None
    profile, _ = match
    assert profile.name == "gemini"
