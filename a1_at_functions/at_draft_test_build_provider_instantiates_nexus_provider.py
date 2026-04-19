# Extracted from C:/!ass-ade/.claude/worktrees/beautiful-dubinsky-c2cb48/a2_mo_composites/mo_draft_testnexusasprovider.py:27
# Component id: at.source.ass_ade.test_build_provider_instantiates_nexus_provider
__version__ = "0.1.0"

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
