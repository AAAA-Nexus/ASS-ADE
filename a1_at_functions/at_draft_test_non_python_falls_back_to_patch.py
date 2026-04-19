# Extracted from C:/!ass-ade/.claude/worktrees/adoring-boyd-0e3a8f/tests/test_version_tracker.py:108
# Component id: at.source.ass_ade.test_non_python_falls_back_to_patch
__version__ = "0.1.0"

    def test_non_python_falls_back_to_patch(self):
        assert classify_change("old code", "new code", language="rust") == "patch"
