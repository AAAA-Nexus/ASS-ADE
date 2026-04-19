# Extracted from C:/!ass-ade/.claude/worktrees/adoring-boyd-0e3a8f/tests/test_tokens.py:23
# Component id: qk.source.ass_ade.test_short_text
__version__ = "0.1.0"

    def test_short_text(self):
        result = estimate_tokens("hello world")
        assert result >= 1
        assert result <= 10
