# Extracted from C:/!ass-ade/.claude/worktrees/adoring-boyd-0e3a8f/tests/test_engine.py:230
# Component id: mo.source.ass_ade.test_fallback_to_ollama
__version__ = "0.1.0"

    def test_fallback_to_ollama(self, monkeypatch):
        """With no keys and all catalog providers disabled, falls back to Ollama."""
        self._clear_provider_env()

        from ass_ade.config import AssAdeConfig

        cfg = self._disable_all_catalog(AssAdeConfig(profile="local"))
        provider = build_provider(cfg)
        assert isinstance(provider, OpenAICompatibleProvider)
