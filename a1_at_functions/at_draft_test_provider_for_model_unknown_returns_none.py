# Extracted from C:/!ass-ade/.claude/worktrees/adoring-boyd-0e3a8f/tests/test_free_providers.py:171
# Component id: at.source.ass_ade.test_provider_for_model_unknown_returns_none
__version__ = "0.1.0"

    def test_provider_for_model_unknown_returns_none(self):
        assert provider_for_model("not-a-real-model") is None
