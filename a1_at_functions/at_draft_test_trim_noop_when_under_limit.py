# Extracted from C:/!ass-ade/.claude/worktrees/beautiful-dubinsky-c2cb48/a2_mo_composites/mo_draft_testconversation.py:36
# Component id: at.source.ass_ade.test_trim_noop_when_under_limit
__version__ = "0.1.0"

    def test_trim_noop_when_under_limit(self):
        c = Conversation("system")
        c.add_user("hello")
        assert c.trim(max_messages=50) == 0
