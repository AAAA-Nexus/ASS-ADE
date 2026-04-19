# Extracted from C:/!ass-ade/.claude/worktrees/adoring-boyd-0e3a8f/tests/test_free_providers.py:166
# Component id: at.source.ass_ade.test_provider_for_model_reverse_lookup
__version__ = "0.1.0"

    def test_provider_for_model_reverse_lookup(self):
        # groq's balanced tier model
        groq_balanced = get_provider("groq").models_by_tier["balanced"]
        assert provider_for_model(groq_balanced) == "groq"
