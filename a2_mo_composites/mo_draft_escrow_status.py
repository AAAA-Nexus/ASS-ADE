# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a2_mo_composites/mo_draft_nexusclient.py:350
# Component id: mo.source.a2_mo_composites.escrow_status
from __future__ import annotations

__version__ = "0.1.0"

def escrow_status(self, escrow_id: str) -> EscrowStatus:
    """/v1/escrow/status/{id} — check escrow state. $0.008/call"""
    return self._get_model(f"/v1/escrow/status/{_pseg(escrow_id, 'escrow_id')}", EscrowStatus)
