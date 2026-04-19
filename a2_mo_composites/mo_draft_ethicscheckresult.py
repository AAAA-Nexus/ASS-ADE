# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a2_mo_composites/mo_draft_ethicscheckresult.py:7
# Component id: mo.source.a2_mo_composites.ethicscheckresult
from __future__ import annotations

__version__ = "0.1.0"

class EthicsCheckResult(NexusModel):
    """/v1/ethics/check and /v1/ethics/compliance"""
    safe: bool | None = None
    score: float | None = None
    axiom_bound: float | None = None
    violations: list[str] = Field(default_factory=list)
