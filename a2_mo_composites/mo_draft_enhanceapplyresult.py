# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a2_mo_composites/mo_draft_enhanceapplyresult.py:7
# Component id: mo.source.a2_mo_composites.enhanceapplyresult
from __future__ import annotations

__version__ = "0.1.0"

class EnhanceApplyResult(NexusModel):
    ok: bool = False
    path: str | None = None
    applied_count: int = 0
    blueprints: list[dict[str, Any]] = []
    rebuild_triggered: bool = False
    certified: bool = False
    lora_captured: bool = False
    credit_used: float | None = None
    message: str | None = None
