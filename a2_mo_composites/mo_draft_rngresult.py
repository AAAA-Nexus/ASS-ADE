# Extracted from C:/!ass-ade/src/ass_ade/nexus/models.py:192
# Component id: mo.source.ass_ade.rngresult
from __future__ import annotations

__version__ = "0.1.0"

class RngResult(NexusModel):
    """/v1/rng/quantum"""
    numbers: list[float] = Field(default_factory=list)
    seed_ts: str | None = None
    proof: str | None = None
    verified: bool | None = None
