# Extracted from C:/!ass-ade/.claude/worktrees/adoring-boyd-0e3a8f/tests/test_free_providers.py:236
# Component id: at.source.ass_ade.test_claude_tier_alias_works
__version__ = "0.1.0"

    def test_claude_tier_alias_works(self, monkeypatch):
        monkeypatch.setenv("GROQ_API_KEY", "sk-a")
        match = select_provider_for_tier("haiku")  # alias for "fast"
        assert match is not None
        profile, model = match
        assert model == profile.models_by_tier["fast"]
