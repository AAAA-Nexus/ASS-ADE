# Extracted from C:/!ass-ade/.claude/worktrees/beautiful-dubinsky-c2cb48/a2_mo_composites/mo_draft_testconfigproviderfields.py:14
# Component id: at.source.ass_ade.test_provider_override_parses_from_json
__version__ = "0.1.0"

    def test_provider_override_parses_from_json(self):
        from ass_ade.config import AssAdeConfig
        cfg = AssAdeConfig.model_validate({
            "profile": "local",
            "providers": {
                "groq": {"enabled": True, "api_key": "sk-test"},
                "gemini": {"enabled": False},
            },
            "tier_policy": {"balanced": "groq"},
            "provider_fallback_chain": ["groq", "gemini", "ollama"],
        })
        assert cfg.providers["groq"].api_key == "sk-test"
        assert cfg.providers["gemini"].enabled is False
        assert cfg.tier_policy == {"balanced": "groq"}
        assert cfg.provider_fallback_chain == ["groq", "gemini", "ollama"]
