# Extracted from C:/!ass-ade/.claude/worktrees/adoring-boyd-0e3a8f/tests/test_tokens.py:48
# Component id: qk.source.ass_ade.test_simple_user_message
__version__ = "0.1.0"

    def test_simple_user_message(self):
        msg = Message(role="user", content="Hello!")
        tokens = estimate_message_tokens(msg)
        assert tokens >= 5  # 4 overhead + at least 1 content
