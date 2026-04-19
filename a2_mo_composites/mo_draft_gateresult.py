# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a2_mo_composites/mo_draft_gateresult.py:7
# Component id: mo.source.a2_mo_composites.gateresult
from __future__ import annotations

__version__ = "0.1.0"

class GateResult:
    """Structured result from a quality gate."""

    gate: str
    passed: bool
    confidence: float = 0.0
    details: dict[str, Any] | None = None
