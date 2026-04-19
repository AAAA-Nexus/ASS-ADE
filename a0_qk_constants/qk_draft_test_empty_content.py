# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a0_qk_constants/qk_draft_testestimatemessagetokens.py:13
# Component id: qk.source.a0_qk_constants.test_empty_content
from __future__ import annotations

__version__ = "0.1.0"

def test_empty_content(self):
    msg = Message(role="assistant", content="")
    tokens = estimate_message_tokens(msg)
    assert tokens == 4  # just overhead
