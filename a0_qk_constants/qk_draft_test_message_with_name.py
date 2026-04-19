# Extracted from C:/!ass-ade/.claude/worktrees/beautiful-dubinsky-c2cb48/a0_qk_constants/qk_draft_testestimatemessagetokens.py:16
# Component id: qk.source.ass_ade.test_message_with_name
__version__ = "0.1.0"

    def test_message_with_name(self):
        msg = Message(role="tool", content="result", name="read_file")
        tokens = estimate_message_tokens(msg)
        assert tokens >= 6  # overhead + name + content
