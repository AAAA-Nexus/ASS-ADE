# Extracted from C:/!ass-ade/.claude/worktrees/beautiful-dubinsky-c2cb48/a0_qk_constants/qk_draft_testcataloginvariants.py:6
# Component id: qk.source.ass_ade.test_catalog_includes_groq_chutes_nexus
__version__ = "0.1.0"

    def test_catalog_includes_groq_chutes_nexus(self):
        """The three most important providers for a no-budget user must be in the catalog."""
        assert "groq" in FREE_PROVIDERS
        assert "chutes" in FREE_PROVIDERS
        assert "nexus" in FREE_PROVIDERS
