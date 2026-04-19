# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a2_mo_composites/mo_draft_quotadrawresult.py:7
# Component id: mo.source.a2_mo_composites.quotadrawresult
from __future__ import annotations

__version__ = "0.1.0"

class QuotaDrawResult(NexusModel):
    """/v1/quota/tree/{id}/draw — QTA-100"""
    drawn: int | None = None
    remaining: int | None = None
    idempotency_key: str | None = None
