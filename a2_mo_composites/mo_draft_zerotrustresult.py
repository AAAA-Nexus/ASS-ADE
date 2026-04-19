# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a2_mo_composites/mo_draft_zerotrustresult.py:7
# Component id: mo.source.a2_mo_composites.zerotrustresult
from __future__ import annotations

__version__ = "0.1.0"

class ZeroTrustResult(NexusModel):
    """/v1/auth/zero-trust"""
    allowed: bool | None = None
    trust_level: str | None = None
    reason: str | None = None
