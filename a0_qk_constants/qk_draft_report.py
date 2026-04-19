# Extracted from C:/!ass-ade/src/ass_ade/agent/proofbridge.py:60
# Component id: qk.source.ass_ade.report
from __future__ import annotations

__version__ = "0.1.0"

def report(self) -> dict:
    return {"engine": "proofbridge", "translations": self._translations}
