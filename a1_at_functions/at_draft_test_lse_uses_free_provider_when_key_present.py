# Extracted from C:/!ass-ade/tests/test_free_providers.py:270
# Component id: at.source.ass_ade.test_lse_uses_free_provider_when_key_present
from __future__ import annotations

__version__ = "0.1.0"

def test_lse_uses_free_provider_when_key_present(self, monkeypatch):
    # Clear all keys, then give only groq
    for p in FREE_PROVIDERS.values():
        if p.api_key_env:
            monkeypatch.delenv(p.api_key_env, raising=False)
    monkeypatch.setenv("GROQ_API_KEY", "sk-test")

    from ass_ade.agent.lse import LSEEngine
    lse = LSEEngine({})
    decision = lse.select(trs_score=0.8, complexity="medium")
    # Should pick the Groq balanced model
    assert decision.provider == "groq"
    expected_model = get_provider("groq").models_by_tier["balanced"]
    assert decision.model == expected_model
