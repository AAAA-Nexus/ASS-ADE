# Extracted from C:/!ass-ade/src/ass_ade/nexus/models.py:436
# Component id: mo.source.ass_ade.ethicscheckresult
from __future__ import annotations

__version__ = "0.1.0"

class EthicsCheckResult(NexusModel):
    """/v1/ethics/check and /v1/ethics/compliance"""
    safe: bool | None = None
    score: float | None = None
    axiom_bound: float | None = None
    violations: list[str] = Field(default_factory=list)
