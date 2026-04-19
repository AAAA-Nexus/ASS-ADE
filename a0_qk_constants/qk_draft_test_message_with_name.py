# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a0_qk_constants/qk_draft_testestimatemessagetokens.py:18
# Component id: qk.source.a0_qk_constants.test_message_with_name
from __future__ import annotations

__version__ = "0.1.0"

def test_message_with_name(self):
    msg = Message(role="tool", content="result", name="read_file")
    tokens = estimate_message_tokens(msg)
    assert tokens >= 6  # overhead + name + content
