# Extracted from C:/!ass-ade/.claude/worktrees/adoring-boyd-0e3a8f/tests/test_version_tracker.py:30
# Component id: at.source.ass_ade.test_minor
__version__ = "0.1.0"

    def test_minor(self):
        assert bump_version("0.1.3", "minor") == "0.2.0"
