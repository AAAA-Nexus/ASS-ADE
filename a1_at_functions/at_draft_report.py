# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a2_mo_composites/mo_draft_trustverificationgate.py:56
# Component id: at.source.a2_mo_composites.report
from __future__ import annotations

__version__ = "0.1.0"

def report(self) -> dict:
    return {
        "engine": "trust_gate",
        "checks": self._checks,
        "denied": self._denied,
    }
