# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a2_mo_composites/mo_draft_delegationvalidation.py:7
# Component id: mo.source.a2_mo_composites.delegationvalidation
from __future__ import annotations

__version__ = "0.1.0"

class DelegationValidation(NexusModel):
    """/v1/identity/delegation/validate and /v1/delegate/verify"""
    valid: bool | None = None
    depth: int | None = None
    depth_limit: int | None = None   # D_MAX = 23
    receipt_id: str | None = None
    capability_attenuated: bool | None = None
    trust_vector: dict | None = None
