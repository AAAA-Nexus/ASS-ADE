# Extracted from C:/!ass-ade/.claude/worktrees/adoring-boyd-0e3a8f/tests/test_engine.py:32
# Component id: mo.source.ass_ade.test_with_tool_calls
__version__ = "0.1.0"

    def test_with_tool_calls(self):
        tc = ToolCallRequest(id="c1", name="read_file", arguments={"path": "a.py"})
        m = Message(role="assistant", content="", tool_calls=[tc])
        assert len(m.tool_calls) == 1
        assert m.tool_calls[0].name == "read_file"
