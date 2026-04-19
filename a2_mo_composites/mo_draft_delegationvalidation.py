# Extracted from C:/!ass-ade/.claude/worktrees/adoring-boyd-0e3a8f/src/ass_ade/nexus/models.py:218
# Component id: mo.source.ass_ade.delegationvalidation
__version__ = "0.1.0"

class DelegationValidation(NexusModel):
    """/v1/identity/delegation/validate and /v1/delegate/verify"""
    valid: bool | None = None
    depth: int | None = None
    depth_limit: int | None = None   # D_MAX = 23
    receipt_id: str | None = None
    capability_attenuated: bool | None = None
    trust_vector: dict | None = None
