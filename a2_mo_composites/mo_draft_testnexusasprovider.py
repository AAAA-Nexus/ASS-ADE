# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a2_mo_composites/mo_draft_testnexusasprovider.py:7
# Component id: mo.source.a2_mo_composites.testnexusasprovider
from __future__ import annotations

__version__ = "0.1.0"

class TestNexusAsProvider:
    """AAAA-Nexus is selectable like any other provider once the user has a key."""

    def test_nexus_available_when_key_set(self, monkeypatch):
        monkeypatch.setenv("AAAA_NEXUS_API_KEY", "an_test_key")
        profile = get_provider("nexus")
        assert profile is not None
        assert profile.is_available() is True

    def test_nexus_unavailable_without_key(self, monkeypatch):
        monkeypatch.delenv("AAAA_NEXUS_API_KEY", raising=False)
        profile = get_provider("nexus")
        assert profile.is_available() is False

    def test_nexus_selectable_via_tier_policy(self, monkeypatch):
        monkeypatch.setenv("AAAA_NEXUS_API_KEY", "an_test_key")
        from ass_ade.agent.lse import LSEEngine

        lse = LSEEngine({"tier_policy": {"deep": "nexus"}})
        decision = lse.select(trs_score=0.3, complexity="critical")
        assert decision.provider == "nexus"

    def test_build_provider_instantiates_nexus_provider(self, monkeypatch):
        for key in ("OPENAI_API_KEY", "ANTHROPIC_API_KEY", "ASS_ADE_PROVIDER_URL"):
            monkeypatch.delenv(key, raising=False)
        for p in FREE_PROVIDERS.values():
            if p.api_key_env:
                monkeypatch.delenv(p.api_key_env, raising=False)
        monkeypatch.setenv("AAAA_NEXUS_API_KEY", "an_test_key")

        from ass_ade.config import AssAdeConfig, ProviderOverride
        from ass_ade.engine.provider import NexusProvider
        from ass_ade.engine.router import build_provider

        # Profile must be non-local for Nexus to wire up
        cfg = AssAdeConfig(profile="hybrid", nexus_api_key="an_test_key")
        # Disable all other catalog providers so Nexus is the only one
        for name in FREE_PROVIDERS:
            if name != "nexus":
                cfg.providers[name] = ProviderOverride(enabled=False)
        provider = build_provider(cfg)
        # With only Nexus enabled, it's returned directly (no MultiProvider wrapper)
        assert isinstance(provider, NexusProvider)

    def test_nexus_is_in_default_fallback_chain(self):
        assert "nexus" in DEFAULT_FALLBACK_CHAIN

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
