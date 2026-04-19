# Extracted from C:/!ass-ade/.claude/worktrees/beautiful-dubinsky-c2cb48/a0_qk_constants/qk_draft_testcataloginvariants.py:12
# Component id: qk.source.ass_ade.test_nexus_is_marked_special
__version__ = "0.1.0"

    def test_nexus_is_marked_special(self):
        """Nexus uses NexusProvider, not OpenAICompatibleProvider."""
        assert FREE_PROVIDERS["nexus"].special is True
