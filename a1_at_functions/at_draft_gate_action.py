# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a1_at_functions/at_draft_gate_action.py:7
# Component id: at.source.a1_at_functions.gate_action
from __future__ import annotations

__version__ = "0.1.0"

def gate_action(self, action: str, cycle_state: dict) -> tuple[bool, str]:
    self.run_audit(cycle_state)
    if self.is_confident:
        return (True, "conviction_met")
    return (
        False,
        f"conviction {self._conviction:.2f} below required {self._conviction_required:.2f}",
    )
