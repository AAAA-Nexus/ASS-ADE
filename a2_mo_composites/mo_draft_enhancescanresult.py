# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a2_mo_composites/mo_draft_enhancescanresult.py:7
# Component id: mo.source.a2_mo_composites.enhancescanresult
from __future__ import annotations

__version__ = "0.1.0"

class EnhanceScanResult(NexusModel):
    ok: bool = False
    path: str | None = None
    total_findings: int = 0
    findings: list[dict[str, Any]] = []
    blueprints_generated: int = 0
    lora_captured: bool = False
    credit_used: float | None = None
    message: str | None = None
