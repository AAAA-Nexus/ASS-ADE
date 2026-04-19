# Extracted from C:/!ass-ade/.claude/worktrees/beautiful-dubinsky-c2cb48/a0_qk_constants/qk_draft_testestimatemessagetokens.py:11
# Component id: qk.source.ass_ade.test_empty_content
__version__ = "0.1.0"

    def test_empty_content(self):
        msg = Message(role="assistant", content="")
        tokens = estimate_message_tokens(msg)
        assert tokens == 4  # just overhead
