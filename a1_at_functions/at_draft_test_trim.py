# Extracted from C:/!ass-ade/.claude/worktrees/beautiful-dubinsky-c2cb48/a2_mo_composites/mo_draft_testconversation.py:25
# Component id: at.source.ass_ade.test_trim
__version__ = "0.1.0"

    def test_trim(self):
        c = Conversation("system")
        for i in range(60):
            c.add_user(f"msg {i}")
        assert c.count() == 61  # 1 system + 60 user
        removed = c.trim(max_messages=10)
        assert removed == 51
        assert c.count() == 10
        # System prompt preserved
        assert c.messages[0].role == "system"
