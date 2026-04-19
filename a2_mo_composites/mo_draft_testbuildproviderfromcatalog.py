# Extracted from C:/!ass-ade/.claude/worktrees/adoring-boyd-0e3a8f/tests/test_free_providers.py:477
# Component id: mo.source.ass_ade.testbuildproviderfromcatalog
__version__ = "0.1.0"

class TestBuildProviderFromCatalog:
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

    def test_no_providers_falls_back_to_ollama(self, monkeypatch):
        for key in ("OPENAI_API_KEY", "ANTHROPIC_API_KEY", "ASS_ADE_PROVIDER_URL"):
            monkeypatch.delenv(key, raising=False)
        for p in FREE_PROVIDERS.values():
            if p.api_key_env:
                monkeypatch.delenv(p.api_key_env, raising=False)
        # Disable every catalog provider
        from ass_ade.config import AssAdeConfig, ProviderOverride
        from ass_ade.engine.router import build_provider
        cfg = AssAdeConfig(profile="local")
        for n in FREE_PROVIDERS:
            cfg.providers[n] = ProviderOverride(enabled=False)
        result = build_provider(cfg)
        # Should fall back to Ollama localhost (an OpenAICompatibleProvider)
        from ass_ade.engine.provider import OpenAICompatibleProvider
        assert isinstance(result, OpenAICompatibleProvider)

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
