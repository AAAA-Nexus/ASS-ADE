# Extracted from C:/!ass-ade/tests/test_free_providers.py:504
# Component id: at.source.ass_ade.test_single_provider_shortcut
from __future__ import annotations

__version__ = "0.1.0"

def test_single_provider_shortcut(self, monkeypatch):
    """When only one provider is available, build_provider returns it directly (no MultiProvider wrapper)."""
    for key in ("OPENAI_API_KEY", "ANTHROPIC_API_KEY", "ASS_ADE_PROVIDER_URL"):
        monkeypatch.delenv(key, raising=False)
    for p in FREE_PROVIDERS.values():
        if p.api_key_env:
            monkeypatch.delenv(p.api_key_env, raising=False)
    # Disable pollinations and ollama to force a single-provider scenario
    from ass_ade.config import AssAdeConfig, ProviderOverride
    from ass_ade.engine.router import build_provider

    cfg = AssAdeConfig(profile="local")
    # Clear available providers except one
    disabled_names = {n for n in FREE_PROVIDERS if n != "groq"}
    for n in disabled_names:
        cfg.providers[n] = ProviderOverride(enabled=False)
    monkeypatch.setenv("GROQ_API_KEY", "sk-groq")

    result = build_provider(cfg)
    # With exactly one provider, expect a direct OpenAICompatibleProvider
    from ass_ade.engine.provider import OpenAICompatibleProvider
    assert isinstance(result, OpenAICompatibleProvider)
