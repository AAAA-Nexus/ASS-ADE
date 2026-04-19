# Extracted from C:/!ass-ade/src/ass_ade/agent/gates.py:52
# Component id: at.source.ass_ade.gate_log
from __future__ import annotations

__version__ = "0.1.0"

def gate_log(self) -> list[GateResult]:
    """Full log of gate results for this session."""
    return list(self._gate_log)
