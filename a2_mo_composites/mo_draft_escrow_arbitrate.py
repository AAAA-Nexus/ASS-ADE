# Extracted from C:/!ass-ade/src/ass_ade/nexus/client.py:561
# Component id: mo.source.ass_ade.escrow_arbitrate
from __future__ import annotations

__version__ = "0.1.0"

def escrow_arbitrate(self, escrow_id: str, vote: str, **kwargs: Any) -> EscrowResult:
    """/v1/escrow/arbitrate — cast arbiter vote (3-vote majority). $0.020/call"""
    return self._post_model("/v1/escrow/arbitrate", EscrowResult, {"escrow_id": escrow_id, "vote": vote, **kwargs})
