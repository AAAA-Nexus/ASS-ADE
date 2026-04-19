# Extracted from C:/!ass-ade/.claude/worktrees/adoring-boyd-0e3a8f/tests/test_engine.py:60
# Component id: mo.source.ass_ade.test_basic
__version__ = "0.1.0"

    def test_basic(self):
        r = CompletionResponse(
            message=Message(role="assistant", content="done"),
            finish_reason="stop",
        )
        assert r.finish_reason == "stop"
        assert r.model is None
