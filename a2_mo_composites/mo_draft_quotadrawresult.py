# Extracted from C:/!ass-ade/src/ass_ade/nexus/models.py:638
# Component id: mo.source.ass_ade.quotadrawresult
from __future__ import annotations

__version__ = "0.1.0"

class QuotaDrawResult(NexusModel):
    """/v1/quota/tree/{id}/draw — QTA-100"""
    drawn: int | None = None
    remaining: int | None = None
    idempotency_key: str | None = None
