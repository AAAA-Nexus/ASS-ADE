# Extracted from C:/!ass-ade/.claude/worktrees/adoring-boyd-0e3a8f/tests/test_free_providers.py:527
# Component id: at.source.ass_ade.test_no_providers_falls_back_to_ollama
__version__ = "0.1.0"

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
