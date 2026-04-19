# Extracted from C:/!ass-ade/src/ass_ade/agent/gates.py:26
# Component id: mo.source.ass_ade.gateresult
from __future__ import annotations

__version__ = "0.1.0"

class GateResult:
    """Structured result from a quality gate."""

    gate: str
    passed: bool
    confidence: float = 0.0
    details: dict[str, Any] | None = None
