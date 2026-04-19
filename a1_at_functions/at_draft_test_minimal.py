# Extracted from C:/!ass-ade/.claude/worktrees/beautiful-dubinsky-c2cb48/a2_mo_composites/mo_draft_testmessage.py:6
# Component id: at.source.ass_ade.test_minimal
__version__ = "0.1.0"

    def test_minimal(self):
        m = Message(role="user", content="hello")
        assert m.role == "user"
        assert m.content == "hello"
        assert m.tool_calls == []
        assert m.tool_call_id is None
