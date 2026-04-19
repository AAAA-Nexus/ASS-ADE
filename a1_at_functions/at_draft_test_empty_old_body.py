# Extracted from C:/!ass-ade/.claude/worktrees/adoring-boyd-0e3a8f/tests/test_version_tracker.py:111
# Component id: at.source.ass_ade.test_empty_old_body
__version__ = "0.1.0"

    def test_empty_old_body(self):
        new = "def foo(): pass"
        result = classify_change("", new)
        assert result in {"minor", "patch"}
