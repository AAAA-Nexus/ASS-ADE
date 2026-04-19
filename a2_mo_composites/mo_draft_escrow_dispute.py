# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a2_mo_composites/mo_draft_nexusclient.py:354
# Component id: mo.source.a2_mo_composites.escrow_dispute
from __future__ import annotations

__version__ = "0.1.0"

def escrow_dispute(
    self,
    escrow_id: str,
    evidence: str | None = None,
    *,
    reason: str | None = None,
    **kwargs: Any,
) -> EscrowResult:
    """/v1/escrow/dispute — open dispute with evidence. $0.060/call"""
    dispute_evidence = evidence or reason or ""
    return self._post_model("/v1/escrow/dispute", EscrowResult, {"escrow_id": escrow_id, "evidence": dispute_evidence, **kwargs})
