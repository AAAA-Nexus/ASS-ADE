# Extracted from C:/!ass-ade/.claude/worktrees/adoring-boyd-0e3a8f/tests/test_tokens.py:110
# Component id: qk.source.ass_ade.test_fuzzy_match
__version__ = "0.1.0"

    def test_fuzzy_match(self):
        # Should match "llama-3.1-8b" as substring
        assert context_window_for("ollama/llama-3.1-8b") == 128_000
