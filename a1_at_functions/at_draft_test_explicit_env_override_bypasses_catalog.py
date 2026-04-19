# Extracted from C:/!ass-ade/tests/test_free_providers.py:544
# Component id: at.source.ass_ade.test_explicit_env_override_bypasses_catalog
from __future__ import annotations

__version__ = "0.1.0"

def test_explicit_env_override_bypasses_catalog(self, monkeypatch):
    monkeypatch.setenv("ASS_ADE_PROVIDER_URL", "https://custom.example.com/v1")
    monkeypatch.setenv("ASS_ADE_PROVIDER_KEY", "custom-key")
    monkeypatch.setenv("GROQ_API_KEY", "sk-groq")

    from ass_ade.config import AssAdeConfig
    from ass_ade.engine.provider import OpenAICompatibleProvider
    from ass_ade.engine.router import build_provider

    cfg = AssAdeConfig(profile="local")
    result = build_provider(cfg)
    # Explicit override wins — should be a single OpenAICompatibleProvider
    assert isinstance(result, OpenAICompatibleProvider)
