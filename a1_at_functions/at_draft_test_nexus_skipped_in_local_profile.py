# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a1_at_functions/at_draft_test_nexus_skipped_in_local_profile.py:7
# Component id: at.source.a1_at_functions.test_nexus_skipped_in_local_profile
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
