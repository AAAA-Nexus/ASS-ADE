# Extracted from C:/!ass-ade/.claude/worktrees/beautiful-dubinsky-c2cb48/a2_mo_composites/mo_draft_authorizeactionresult.py:5
# Component id: mo.source.ass_ade.authorizeactionresult
__version__ = "0.1.0"

class AuthorizeActionResult(NexusModel):
    """/v1/authorize/action — OAP-100"""
    decision: str | None = None   # "allow" | "deny"
    risk_tier: str | None = None
    delegation_depth_ok: bool | None = None
    identity_check_passed: bool | None = None
