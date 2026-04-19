# Extracted from C:/!ass-ade/.claude/worktrees/beautiful-dubinsky-c2cb48/a2_mo_composites/mo_draft_testchutesprovider.py:16
# Component id: at.source.ass_ade.test_chutes_serves_deepseek_models
__version__ = "0.1.0"

    def test_chutes_serves_deepseek_models(self):
        profile = get_provider("chutes")
        assert "deepseek" in profile.models_by_tier["balanced"].lower()
        assert "deepseek" in profile.models_by_tier["deep"].lower()
