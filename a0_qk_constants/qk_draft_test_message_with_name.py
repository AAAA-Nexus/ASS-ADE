# Extracted from C:/!ass-ade/tests/test_tokens.py:58
# Component id: qk.source.ass_ade.test_message_with_name
from __future__ import annotations

__version__ = "0.1.0"

def test_message_with_name(self):
    msg = Message(role="tool", content="result", name="read_file")
    tokens = estimate_message_tokens(msg)
    assert tokens >= 6  # overhead + name + content
