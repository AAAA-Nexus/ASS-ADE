# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a2_mo_composites/mo_draft_hallucinationresult.py:7
# Component id: mo.source.a2_mo_composites.hallucinationresult
from __future__ import annotations

__version__ = "0.1.0"

class HallucinationResult(NexusModel):
    """/v1/oracle/hallucination"""
    policy_epsilon: float | None = None
    verdict: str | None = None       # "safe" | "caution" | "unsafe"
    ceiling: str | None = None       # "proved-not-estimated"
    confidence: float | None = None
