# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a2_mo_composites/mo_draft_authorizeactionresult.py:7
# Component id: mo.source.a2_mo_composites.authorizeactionresult
from __future__ import annotations

__version__ = "0.1.0"

class AuthorizeActionResult(NexusModel):
    """/v1/authorize/action — OAP-100"""
    decision: str | None = None   # "allow" | "deny"
    risk_tier: str | None = None
    delegation_depth_ok: bool | None = None
    identity_check_passed: bool | None = None
