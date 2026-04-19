# Extracted from C:/!ass-ade/src/ass_ade/nexus/client.py:541
# Component id: mo.source.ass_ade.escrow_release
from __future__ import annotations

__version__ = "0.1.0"

def escrow_release(self, escrow_id: str, proof: str, **kwargs: Any) -> EscrowResult:
    """/v1/escrow/release — release funds with completion proof. $0.020/call"""
    return self._post_model("/v1/escrow/release", EscrowResult, {"escrow_id": escrow_id, "proof": proof, **kwargs})
