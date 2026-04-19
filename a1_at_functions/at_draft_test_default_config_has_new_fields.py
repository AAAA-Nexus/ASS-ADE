# Extracted from C:/!ass-ade/.claude/worktrees/beautiful-dubinsky-c2cb48/a2_mo_composites/mo_draft_testconfigproviderfields.py:6
# Component id: at.source.ass_ade.test_default_config_has_new_fields
__version__ = "0.1.0"

    def test_default_config_has_new_fields(self):
        from ass_ade.config import AssAdeConfig
        cfg = AssAdeConfig()
        assert cfg.lse_enabled is True
        assert cfg.tier_policy == {}
        assert cfg.provider_fallback_chain == []
        assert cfg.providers == {}
