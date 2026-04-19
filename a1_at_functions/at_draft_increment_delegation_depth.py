# Extracted from C:/!ass-ade/src/ass_ade/agent/loop.py:143
# Component id: at.source.ass_ade.increment_delegation_depth
from __future__ import annotations

__version__ = "0.1.0"

def increment_delegation_depth(self) -> bool:
    """Increment delegation depth. Returns False if D_MAX=23 exceeded."""
    self._delegation_depth += 1
    return self._delegation_depth <= D_MAX
