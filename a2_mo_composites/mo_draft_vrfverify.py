# Extracted from C:/!ass-ade/src/ass_ade/nexus/models.py:209
# Component id: mo.source.ass_ade.vrfverify
from __future__ import annotations

__version__ = "0.1.0"

class VrfVerify(NexusModel):
    """/v1/vrf/verify-draw"""
    valid: bool | None = None
    draw_id: str | None = None
    proof: str | None = None
