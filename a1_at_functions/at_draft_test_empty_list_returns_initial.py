# Extracted from C:/!ass-ade/.claude/worktrees/adoring-boyd-0e3a8f/tests/test_version_tracker.py:187
# Component id: at.source.ass_ade.test_empty_list_returns_initial
__version__ = "0.1.0"

    def test_empty_list_returns_initial(self):
        assert _aggregate_version([]) == INITIAL_VERSION
