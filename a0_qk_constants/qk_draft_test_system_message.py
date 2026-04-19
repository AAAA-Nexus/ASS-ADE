# Extracted from C:/!ass-ade/tests/test_tokens.py:63
# Component id: qk.source.ass_ade.test_system_message
from __future__ import annotations

__version__ = "0.1.0"

def test_system_message(self):
    msg = Message(role="system", content="You are an AI assistant.")
    tokens = estimate_message_tokens(msg)
    assert tokens >= 5
