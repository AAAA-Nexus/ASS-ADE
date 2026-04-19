# Extracted from C:/!ass-ade/src/ass_ade/agent/lse.py:61
# Component id: mo.source.ass_ade.lsedecision
from __future__ import annotations

__version__ = "0.1.0"

class LSEDecision:
    model: str
    tier: str
    reason: str
    trs_score: float
    complexity: str
    provider: str | None = None  # provider name from catalog (e.g., "groq")
