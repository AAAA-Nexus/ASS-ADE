# Extracted from C:/!ass-ade/.claude/worktrees/adoring-boyd-0e3a8f/tests/test_version_tracker.py:27
# Component id: at.source.ass_ade.test_patch
__version__ = "0.1.0"

    def test_patch(self):
        assert bump_version("0.1.3", "patch") == "0.1.4"
