# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a0_qk_constants/qk_draft_testestimatemessagetokens.py:23
# Component id: qk.source.a0_qk_constants.test_system_message
from __future__ import annotations

__version__ = "0.1.0"

def test_system_message(self):
    msg = Message(role="system", content="You are an AI assistant.")
    tokens = estimate_message_tokens(msg)
    assert tokens >= 5
