# Extracted from C:/!ass-ade/.claude/worktrees/adoring-boyd-0e3a8f/tests/test_tokens.py:104
# Component id: qk.source.ass_ade.test_unknown_model
__version__ = "0.1.0"

    def test_unknown_model(self):
        assert context_window_for("totally-unknown-model") == DEFAULT_CONTEXT_WINDOW
