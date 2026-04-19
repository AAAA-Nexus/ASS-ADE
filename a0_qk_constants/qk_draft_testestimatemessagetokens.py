# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a0_qk_constants/qk_draft_testestimatemessagetokens.py:7
# Component id: qk.source.a0_qk_constants.testestimatemessagetokens
from __future__ import annotations

__version__ = "0.1.0"

class TestEstimateMessageTokens:
    def test_simple_user_message(self):
        msg = Message(role="user", content="Hello!")
        tokens = estimate_message_tokens(msg)
        assert tokens >= 5  # 4 overhead + at least 1 content

    def test_empty_content(self):
        msg = Message(role="assistant", content="")
        tokens = estimate_message_tokens(msg)
        assert tokens == 4  # just overhead

    def test_message_with_name(self):
        msg = Message(role="tool", content="result", name="read_file")
        tokens = estimate_message_tokens(msg)
        assert tokens >= 6  # overhead + name + content

    def test_system_message(self):
        msg = Message(role="system", content="You are an AI assistant.")
        tokens = estimate_message_tokens(msg)
        assert tokens >= 5
