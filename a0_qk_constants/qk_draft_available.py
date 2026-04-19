# Extracted from C:/!ass-ade/src/ass_ade/engine/tokens.py:189
# Component id: qk.source.ass_ade.available
from __future__ import annotations

__version__ = "0.1.0"

def available(self) -> int:
    """Tokens available for prompt content (messages + tools)."""
    return max(0, self.context_window - self.reserve)
