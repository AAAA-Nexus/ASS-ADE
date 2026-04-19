# Extracted from C:/!ass-ade/.claude/worktrees/adoring-boyd-0e3a8f/tests/test_engine.py:25
# Component id: mo.source.ass_ade.test_minimal
__version__ = "0.1.0"

    def test_minimal(self):
        m = Message(role="user", content="hello")
        assert m.role == "user"
        assert m.content == "hello"
        assert m.tool_calls == []
        assert m.tool_call_id is None
