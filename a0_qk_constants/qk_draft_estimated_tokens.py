# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a0_qk_constants/qk_draft_estimated_tokens.py:7
# Component id: qk.source.a0_qk_constants.estimated_tokens
from __future__ import annotations

__version__ = "0.1.0"

def estimated_tokens(self) -> int:
    """Total estimated tokens across all messages."""
    return sum(estimate_message_tokens(m) for m in self._messages)
