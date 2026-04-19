# Extracted from C:/!ass-ade/.claude/worktrees/adoring-boyd-0e3a8f/tests/test_free_providers.py:174
# Component id: at.source.ass_ade.test_provider_for_model_empty_string
__version__ = "0.1.0"

    def test_provider_for_model_empty_string(self):
        assert provider_for_model("") is None
