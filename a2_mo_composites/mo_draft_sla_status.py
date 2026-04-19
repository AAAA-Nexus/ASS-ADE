# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a2_mo_composites/mo_draft_nexusclient.py:403
# Component id: mo.source.a2_mo_composites.sla_status
from __future__ import annotations

__version__ = "0.1.0"

def sla_status(self, sla_id: str) -> SlaStatus:
    """/v1/sla/status/{id} — compliance score + bond remaining. $0.008/call"""
    return self._get_model(f"/v1/sla/status/{_pseg(sla_id, 'sla_id')}", SlaStatus)
