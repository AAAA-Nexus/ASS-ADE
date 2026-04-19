# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a2_mo_composites/mo_draft_ratchetproberesult.py:7
# Component id: mo.source.a2_mo_composites.ratchetproberesult
from __future__ import annotations

__version__ = "0.1.0"

class RatchetProbeResult(NexusModel):
    """/v1/ratchet/probe — batch health check"""
    results: list[dict] = Field(default_factory=list)
