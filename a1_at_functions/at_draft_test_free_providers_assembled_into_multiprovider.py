# Extracted from C:/!ass-ade/tests/test_free_providers.py:478
# Component id: at.source.ass_ade.test_free_providers_assembled_into_multiprovider
from __future__ import annotations

__version__ = "0.1.0"

def test_free_providers_assembled_into_multiprovider(self, monkeypatch):
    # Clear paid keys so we don't hit the legacy path
    for key in ("OPENAI_API_KEY", "ANTHROPIC_API_KEY", "ASS_ADE_PROVIDER_URL"):
        monkeypatch.delenv(key, raising=False)
    # Clear every cloud catalog key, then set only groq
    for p in FREE_PROVIDERS.values():
        if p.api_key_env:
            monkeypatch.delenv(p.api_key_env, raising=False)
    monkeypatch.setenv("GROQ_API_KEY", "sk-groq")
    monkeypatch.setenv("GEMINI_API_KEY", "sk-gemini")

    from ass_ade.config import AssAdeConfig
    from ass_ade.engine.provider import MultiProvider
    from ass_ade.engine.router import build_provider

    cfg = AssAdeConfig(profile="local")
    result = build_provider(cfg)
    # With multiple providers, should build a MultiProvider
    assert isinstance(result, MultiProvider)
    # Should contain both groq and gemini
    names = set(result.providers.keys())
    assert "groq" in names
    assert "gemini" in names
    # Pollinations (no-key) should also be present as a fallback
    assert "pollinations" in names
