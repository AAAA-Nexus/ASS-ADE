# Extracted from C:/!ass-ade/.claude/worktrees/beautiful-dubinsky-c2cb48/a0_qk_constants/qk_draft_testestimatemessagetokens.py:21
# Component id: qk.source.ass_ade.test_system_message
__version__ = "0.1.0"

    def test_system_message(self):
        msg = Message(role="system", content="You are an AI assistant.")
        tokens = estimate_message_tokens(msg)
        assert tokens >= 5
