# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a1_at_functions/at_draft_gate_log.py:7
# Component id: at.source.a1_at_functions.gate_log
from __future__ import annotations

__version__ = "0.1.0"

def gate_log(self) -> list[GateResult]:
    """Full log of gate results for this session."""
    return list(self._gate_log)
