# Extracted from C:/!ass-ade/tests/test_free_providers.py:611
# Component id: at.source.ass_ade.test_nexus_skipped_in_local_profile
from __future__ import annotations

__version__ = "0.1.0"

def test_nexus_skipped_in_local_profile(self, monkeypatch):
    """Nexus is a metered paid-ish provider; local profile should skip it."""
    for key in ("OPENAI_API_KEY", "ANTHROPIC_API_KEY"):
        monkeypatch.delenv(key, raising=False)
    for p in FREE_PROVIDERS.values():
        if p.api_key_env:
            monkeypatch.delenv(p.api_key_env, raising=False)
    monkeypatch.setenv("AAAA_NEXUS_API_KEY", "an_test_key")

    from ass_ade.config import AssAdeConfig
    from ass_ade.engine.router import build_provider

    cfg = AssAdeConfig(profile="local", nexus_api_key="an_test_key")
    provider = build_provider(cfg)
    # Nexus must not be in the provider map when profile is local
    if hasattr(provider, "providers"):
        assert "nexus" not in provider.providers
