# Extracted from C:/!ass-ade/tests/test_free_providers.py:184
# Component id: at.source.ass_ade.test_selects_first_available_in_chain
from __future__ import annotations

__version__ = "0.1.0"

def test_selects_first_available_in_chain(self, monkeypatch):
    # Clear all cloud keys
    for p in FREE_PROVIDERS.values():
        if p.api_key_env:
            monkeypatch.delenv(p.api_key_env, raising=False)
    # Give only groq a key
    monkeypatch.setenv("GROQ_API_KEY", "sk-test")
    match = select_provider_for_tier("balanced")
    assert match is not None
    profile, model = match
    assert profile.name == "groq"
    assert model == profile.models_by_tier["balanced"]
