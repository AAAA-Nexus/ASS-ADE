# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a0_qk_constants/qk_draft_test_simple_user_message.py:7
# Component id: qk.source.a0_qk_constants.test_simple_user_message
from __future__ import annotations

__version__ = "0.1.0"

def test_simple_user_message(self):
    msg = Message(role="user", content="Hello!")
    tokens = estimate_message_tokens(msg)
    assert tokens >= 5  # 4 overhead + at least 1 content
