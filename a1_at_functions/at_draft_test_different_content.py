# Extracted from C:/!ass-ade/.claude/worktrees/adoring-boyd-0e3a8f/tests/test_version_tracker.py:52
# Component id: at.source.ass_ade.test_different_content
__version__ = "0.1.0"

    def test_different_content(self):
        assert content_hash("foo") != content_hash("bar")
