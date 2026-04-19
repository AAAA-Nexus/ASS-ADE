# Extracted from C:/!ass-ade/src/ass_ade/agent/trust_gate.py:56
# Component id: at.source.ass_ade.report
from __future__ import annotations

__version__ = "0.1.0"

def report(self) -> dict:
    return {
        "engine": "trust_gate",
        "checks": self._checks,
        "denied": self._denied,
    }
