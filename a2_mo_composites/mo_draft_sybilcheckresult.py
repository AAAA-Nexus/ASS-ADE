# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a2_mo_composites/mo_draft_sybilcheckresult.py:7
# Component id: mo.source.a2_mo_composites.sybilcheckresult
from __future__ import annotations

__version__ = "0.1.0"

class SybilCheckResult(NexusModel):
    """/v1/identity/sybil-check"""
    sybil_risk: str | None = None   # "low" | "medium" | "high"
    score: float | None = None
    flags: list[str] = Field(default_factory=list)
