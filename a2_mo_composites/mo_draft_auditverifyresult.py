# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a2_mo_composites/mo_draft_auditverifyresult.py:7
# Component id: mo.source.a2_mo_composites.auditverifyresult
from __future__ import annotations

__version__ = "0.1.0"

class AuditVerifyResult(NexusModel):
    """/v1/audit/verify"""
    intact: bool | None = None
    chain_length: int | None = None
    first_entry: str | None = None
    last_entry: str | None = None
