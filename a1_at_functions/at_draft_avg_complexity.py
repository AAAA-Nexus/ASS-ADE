# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a1_at_functions/at_draft_avg_complexity.py:7
# Component id: at.source.a1_at_functions.avg_complexity
from __future__ import annotations

__version__ = "0.1.0"

def avg_complexity(self) -> float:
    """Average complexity across all routed messages."""
    if not self._history:
        return 0.0
    return sum(d.complexity for d in self._history) / len(self._history)
