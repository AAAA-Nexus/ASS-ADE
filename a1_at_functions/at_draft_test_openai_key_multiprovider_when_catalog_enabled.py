# Extracted from C:/!ass-ade/.claude/worktrees/beautiful-dubinsky-c2cb48/a2_mo_composites/mo_draft_testbuildprovider.py:42
# Component id: at.source.ass_ade.test_openai_key_multiprovider_when_catalog_enabled
__version__ = "0.1.0"

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
