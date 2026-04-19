# Extracted from C:/!ass-ade/tests/test_tokens.py:53
# Component id: qk.source.ass_ade.test_empty_content
from __future__ import annotations

__version__ = "0.1.0"

def test_empty_content(self):
    msg = Message(role="assistant", content="")
    tokens = estimate_message_tokens(msg)
    assert tokens == 4  # just overhead
