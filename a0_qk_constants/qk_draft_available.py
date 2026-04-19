# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a0_qk_constants/qk_draft_available.py:7
# Component id: qk.source.a0_qk_constants.available
from __future__ import annotations

__version__ = "0.1.0"

def available(self) -> int:
    """Tokens available for prompt content (messages + tools)."""
    return max(0, self.context_window - self.reserve)
