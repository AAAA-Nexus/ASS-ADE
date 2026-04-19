# Extracted from C:/!ass-ade/.claude/worktrees/adoring-boyd-0e3a8f/tests/test_tokens.py:20
# Component id: qk.source.ass_ade.test_empty_string
__version__ = "0.1.0"

    def test_empty_string(self):
        assert estimate_tokens("") == 1  # min 1
