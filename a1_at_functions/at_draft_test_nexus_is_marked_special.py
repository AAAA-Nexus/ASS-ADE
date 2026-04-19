# Extracted from C:/!ass-ade/.claude/worktrees/adoring-boyd-0e3a8f/tests/test_free_providers.py:40
# Component id: at.source.ass_ade.test_nexus_is_marked_special
__version__ = "0.1.0"

    def test_nexus_is_marked_special(self):
        """Nexus uses NexusProvider, not OpenAICompatibleProvider."""
        assert FREE_PROVIDERS["nexus"].special is True
