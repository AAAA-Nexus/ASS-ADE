# Extracted from C:/!ass-ade/src/ass_ade/agent/conversation.py:57
# Component id: qk.source.ass_ade.estimated_tokens
from __future__ import annotations

__version__ = "0.1.0"

def estimated_tokens(self) -> int:
    """Total estimated tokens across all messages."""
    return sum(estimate_message_tokens(m) for m in self._messages)
