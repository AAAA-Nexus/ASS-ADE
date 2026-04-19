# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a2_mo_composites/mo_draft_rngresult.py:7
# Component id: mo.source.a2_mo_composites.rngresult
from __future__ import annotations

__version__ = "0.1.0"

class RngResult(NexusModel):
    """/v1/rng/quantum"""
    numbers: list[float] = Field(default_factory=list)
    seed_ts: str | None = None
    proof: str | None = None
    verified: bool | None = None
