# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a2_mo_composites/mo_draft_nexusclient.py:346
# Component id: mo.source.a2_mo_composites.escrow_release
from __future__ import annotations

__version__ = "0.1.0"

def escrow_release(self, escrow_id: str, proof: str, **kwargs: Any) -> EscrowResult:
    """/v1/escrow/release — release funds with completion proof. $0.020/call"""
    return self._post_model("/v1/escrow/release", EscrowResult, {"escrow_id": escrow_id, "proof": proof, **kwargs})
