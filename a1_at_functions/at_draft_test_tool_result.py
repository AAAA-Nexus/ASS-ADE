# Extracted from C:/!ass-ade/.claude/worktrees/beautiful-dubinsky-c2cb48/a2_mo_composites/mo_draft_testmessage.py:19
# Component id: at.source.ass_ade.test_tool_result
__version__ = "0.1.0"

    def test_tool_result(self):
        m = Message(role="tool", content="file data", tool_call_id="c1", name="read_file")
        assert m.role == "tool"
        assert m.tool_call_id == "c1"
