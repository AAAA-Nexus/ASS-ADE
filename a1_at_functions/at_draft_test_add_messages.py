# Extracted from C:/!ass-ade/.claude/worktrees/beautiful-dubinsky-c2cb48/a2_mo_composites/mo_draft_testconversation.py:11
# Component id: at.source.ass_ade.test_add_messages
__version__ = "0.1.0"

    def test_add_messages(self):
        c = Conversation()
        c.add_user("hello")
        c.add_assistant(Message(role="assistant", content="hi"))
        assert c.count() == 2
