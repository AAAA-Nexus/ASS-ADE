# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a1_at_functions/at_draft_increment_delegation_depth.py:7
# Component id: at.source.a1_at_functions.increment_delegation_depth
from __future__ import annotations

__version__ = "0.1.0"

def increment_delegation_depth(self) -> bool:
    """Increment delegation depth. Returns False if D_MAX=23 exceeded."""
    self._delegation_depth += 1
    return self._delegation_depth <= D_MAX
