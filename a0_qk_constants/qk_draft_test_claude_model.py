# Extracted from C:/!ass-ade/.claude/worktrees/adoring-boyd-0e3a8f/tests/test_tokens.py:101
# Component id: qk.source.ass_ade.test_claude_model
__version__ = "0.1.0"

    def test_claude_model(self):
        assert context_window_for("claude-opus-4") == 200_000
