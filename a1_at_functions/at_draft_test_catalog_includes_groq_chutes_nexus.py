# Extracted from C:/!ass-ade/.claude/worktrees/adoring-boyd-0e3a8f/tests/test_free_providers.py:34
# Component id: at.source.ass_ade.test_catalog_includes_groq_chutes_nexus
__version__ = "0.1.0"

    def test_catalog_includes_groq_chutes_nexus(self):
        """The three most important providers for a no-budget user must be in the catalog."""
        assert "groq" in FREE_PROVIDERS
        assert "chutes" in FREE_PROVIDERS
        assert "nexus" in FREE_PROVIDERS
