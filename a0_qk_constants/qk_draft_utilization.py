# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a0_qk_constants/qk_draft_utilization.py:7
# Component id: qk.source.a0_qk_constants.utilization
from __future__ import annotations

__version__ = "0.1.0"

def utilization(self) -> float:
    """Fraction of context window currently used (0.0 – 1.0)."""
    if self.context_window == 0:
        return 1.0
    return min(1.0, self.prompt_tokens / self.context_window)
