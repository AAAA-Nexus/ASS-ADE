# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a2_mo_composites/mo_draft_testbuildprovider.py:7
# Component id: mo.source.a2_mo_composites.testbuildprovider
from __future__ import annotations

__version__ = "0.1.0"

class TestBuildProvider:
    def _clear_provider_env(self) -> None:
        """Remove every provider env var so the test state is deterministic."""
        import os
        from ass_ade.agent.providers import FREE_PROVIDERS
        for key in ("OPENAI_API_KEY", "ANTHROPIC_API_KEY", "ASS_ADE_PROVIDER_URL"):
            os.environ.pop(key, None)
        for p in FREE_PROVIDERS.values():
            if p.api_key_env:
                os.environ.pop(p.api_key_env, None)

    def _disable_all_catalog(self, cfg, *, keep: tuple[str, ...] = ()):
        """Disable every catalog provider so the test isolates a single backend.

        `keep` is a tuple of names to leave enabled (e.g., ('nexus',) to test
        a Nexus-only setup).
        """
        from ass_ade.agent.providers import FREE_PROVIDERS
        from ass_ade.config import ProviderOverride
        for name in FREE_PROVIDERS:
            if name in keep:
                continue
            cfg.providers[name] = ProviderOverride(enabled=False)
        return cfg

    def test_openai_key_picks_openai(self, monkeypatch):
        self._clear_provider_env()
        monkeypatch.setenv("OPENAI_API_KEY", "sk-test")

        from ass_ade.config import AssAdeConfig
        from ass_ade.engine.provider import MultiProvider

        cfg = self._disable_all_catalog(AssAdeConfig(profile="local"))
        provider = build_provider(cfg)
        # With catalog disabled and only OPENAI_API_KEY set, should get a single provider
        assert isinstance(provider, OpenAICompatibleProvider)

    def test_openai_key_multiprovider_when_catalog_enabled(self, monkeypatch):
        """With catalog providers AND OpenAI key, build_provider returns MultiProvider."""
        self._clear_provider_env()
        monkeypatch.setenv("OPENAI_API_KEY", "sk-test")
        monkeypatch.setenv("GROQ_API_KEY", "sk-groq")

        from ass_ade.config import AssAdeConfig
        from ass_ade.engine.provider import MultiProvider

        cfg = AssAdeConfig(profile="local")
        provider = build_provider(cfg)
        assert isinstance(provider, MultiProvider)
        assert "openai" in provider.providers
        assert "groq" in provider.providers

    def test_fallback_to_ollama(self, monkeypatch):
        """With no keys and all catalog providers disabled, falls back to Ollama."""
        self._clear_provider_env()

        from ass_ade.config import AssAdeConfig

        cfg = self._disable_all_catalog(AssAdeConfig(profile="local"))
        provider = build_provider(cfg)
        assert isinstance(provider, OpenAICompatibleProvider)

    def test_nexus_provider_for_premium(self, monkeypatch):
        self._clear_provider_env()
        monkeypatch.setenv("AAAA_NEXUS_API_KEY", "an_test_key")

        from ass_ade.config import AssAdeConfig

        cfg = self._disable_all_catalog(
            AssAdeConfig(
                profile="premium",
                nexus_api_key="an_test_key",
                nexus_base_url="https://atomadic.tech",
            ),
            keep=("nexus",),  # leave Nexus enabled
        )
        provider = build_provider(cfg)
        # Only Nexus enabled → single return
        assert isinstance(provider, NexusProvider)

    def test_nexus_added_to_multiprovider_when_catalog_keys_present(self, monkeypatch):
        """Premium profile + catalog keys → MultiProvider containing nexus + free providers."""
        self._clear_provider_env()
        monkeypatch.setenv("GROQ_API_KEY", "sk-groq")
        monkeypatch.setenv("AAAA_NEXUS_API_KEY", "an_test_key")

        from ass_ade.config import AssAdeConfig
        from ass_ade.engine.provider import MultiProvider

        cfg = AssAdeConfig(
            profile="premium",
            nexus_api_key="an_test_key",
            nexus_base_url="https://atomadic.tech",
        )
        provider = build_provider(cfg)
        assert isinstance(provider, MultiProvider)
        assert "nexus" in provider.providers
        assert "groq" in provider.providers
