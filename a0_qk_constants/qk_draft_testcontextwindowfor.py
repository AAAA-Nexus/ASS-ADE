# Extracted from C:/!ass-ade/.claude/worktrees/beautiful-dubinsky-c2cb48/a0_qk_constants/qk_draft_testcontextwindowfor.py:5
# Component id: qk.source.ass_ade.testcontextwindowfor
__version__ = "0.1.0"

class TestContextWindowFor:
    def test_known_model(self):
        assert context_window_for("gpt-4o") == 128_000

    def test_claude_model(self):
        assert context_window_for("claude-opus-4") == 200_000

    def test_unknown_model(self):
        assert context_window_for("totally-unknown-model") == DEFAULT_CONTEXT_WINDOW

    def test_none_model(self):
        assert context_window_for(None) == DEFAULT_CONTEXT_WINDOW

    def test_fuzzy_match(self):
        # Should match "llama-3.1-8b" as substring
        assert context_window_for("ollama/llama-3.1-8b") == 128_000

    def test_case_insensitive(self):
        assert context_window_for("GPT-4O") == 128_000
