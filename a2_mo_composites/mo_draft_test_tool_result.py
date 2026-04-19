# Extracted from C:/!ass-ade/.claude/worktrees/adoring-boyd-0e3a8f/tests/test_engine.py:38
# Component id: mo.source.ass_ade.test_tool_result
__version__ = "0.1.0"

    def test_tool_result(self):
        m = Message(role="tool", content="file data", tool_call_id="c1", name="read_file")
        assert m.role == "tool"
        assert m.tool_call_id == "c1"
