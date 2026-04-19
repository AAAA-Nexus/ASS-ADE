# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a1_at_functions/at_draft_compute_coefficient.py:7
# Component id: at.source.a1_at_functions.compute_coefficient
from __future__ import annotations

__version__ = "0.1.0"

def compute_coefficient(self) -> float:
    history = self._state.get("history") or []
    if not history:
        return max(1e-6, float(self._state.get("coefficient", 1.0)))
    recent = history[-20:]
    deltas = [float(h.get("delta", 0.0)) for h in recent]
    avg = sum(deltas) / len(deltas)
    base = float(self._state.get("coefficient", 1.0))
    coef = max(1e-6, base * (1.0 + avg))
    self._state["coefficient"] = coef
    return coef
