# Extracted from C:/!ass-ade/.claude/worktrees/beautiful-dubinsky-c2cb48/a2_mo_composites/mo_draft_testconversation.py:17
# Component id: at.source.ass_ade.test_add_tool_result
__version__ = "0.1.0"

    def test_add_tool_result(self):
        c = Conversation()
        c.add_tool_result("c1", "read_file", "file data")
        m = c.messages[-1]
        assert m.role == "tool"
        assert m.tool_call_id == "c1"
        assert m.name == "read_file"
