# Extracted from C:/!ass-ade/src/ass_ade/nexus/models.py:538
# Component id: mo.source.ass_ade.authorizeactionresult
from __future__ import annotations

__version__ = "0.1.0"

class AuthorizeActionResult(NexusModel):
    """/v1/authorize/action — OAP-100"""
    decision: str | None = None   # "allow" | "deny"
    risk_tier: str | None = None
    delegation_depth_ok: bool | None = None
    identity_check_passed: bool | None = None
