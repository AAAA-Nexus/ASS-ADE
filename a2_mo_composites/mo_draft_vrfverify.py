# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a2_mo_composites/mo_draft_vrfverify.py:7
# Component id: mo.source.a2_mo_composites.vrfverify
from __future__ import annotations

__version__ = "0.1.0"

class VrfVerify(NexusModel):
    """/v1/vrf/verify-draw"""
    valid: bool | None = None
    draw_id: str | None = None
    proof: str | None = None
