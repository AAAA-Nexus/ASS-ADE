# Extracted from C:/!ass-ade/.claude/worktrees/beautiful-dubinsky-c2cb48/a2_mo_composites/mo_draft_testbuildprovider.py:30
# Component id: at.source.ass_ade.test_openai_key_picks_openai
__version__ = "0.1.0"

    def test_openai_key_picks_openai(self, monkeypatch):
        self._clear_provider_env()
        monkeypatch.setenv("OPENAI_API_KEY", "sk-test")

        from ass_ade.config import AssAdeConfig
        from ass_ade.engine.provider import MultiProvider

        cfg = self._disable_all_catalog(AssAdeConfig(profile="local"))
        provider = build_provider(cfg)
        # With catalog disabled and only OPENAI_API_KEY set, should get a single provider
        assert isinstance(provider, OpenAICompatibleProvider)
