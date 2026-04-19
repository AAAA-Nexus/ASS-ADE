# Extracted from C:/!ass-ade/tests/test_free_providers.py:224
# Component id: at.source.ass_ade.test_custom_fallback_chain_respected
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
