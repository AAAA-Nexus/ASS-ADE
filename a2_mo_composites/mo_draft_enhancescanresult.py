# Extracted from C:/!ass-ade/src/ass_ade/nexus/models.py:1159
# Component id: mo.source.ass_ade.enhancescanresult
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
