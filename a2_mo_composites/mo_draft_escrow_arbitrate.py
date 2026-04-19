# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a2_mo_composites/mo_draft_nexusclient.py:366
# Component id: mo.source.a2_mo_composites.escrow_arbitrate
from __future__ import annotations

__version__ = "0.1.0"

def escrow_arbitrate(self, escrow_id: str, vote: str, **kwargs: Any) -> EscrowResult:
    """/v1/escrow/arbitrate — cast arbiter vote (3-vote majority). $0.020/call"""
    return self._post_model("/v1/escrow/arbitrate", EscrowResult, {"escrow_id": escrow_id, "vote": vote, **kwargs})
