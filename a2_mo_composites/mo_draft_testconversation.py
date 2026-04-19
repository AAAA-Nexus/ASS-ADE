# Extracted from C:/!ass-ade/.claude/worktrees/adoring-boyd-0e3a8f/tests/test_agent.py:23
# Component id: mo.source.ass_ade.testconversation
__version__ = "0.1.0"

class TestConversation:
    def test_system_prompt(self):
        c = Conversation("You are helpful.")
        assert c.count() == 1
        assert c.messages[0].role == "system"

    def test_add_messages(self):
        c = Conversation()
        c.add_user("hello")
        c.add_assistant(Message(role="assistant", content="hi"))
        assert c.count() == 2

    def test_add_tool_result(self):
        c = Conversation()
        c.add_tool_result("c1", "read_file", "file data")
        m = c.messages[-1]
        assert m.role == "tool"
        assert m.tool_call_id == "c1"
        assert m.name == "read_file"

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

    def test_trim_noop_when_under_limit(self):
        c = Conversation("system")
        c.add_user("hello")
        assert c.trim(max_messages=50) == 0
