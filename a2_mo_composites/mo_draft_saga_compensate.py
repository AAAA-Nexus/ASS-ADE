# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a2_mo_composites/mo_draft_nexusclient.py:704
# Component id: mo.source.a2_mo_composites.saga_compensate
from __future__ import annotations

__version__ = "0.1.0"

def saga_compensate(self, saga_id: str, **kwargs: Any) -> CompensationResult:
    """/v1/rollback/saga/{id}/compensate — LIFO rollback (RBK-100). $0.040/call"""
    return self._post_model(f"/v1/rollback/saga/{_pseg(saga_id, 'saga_id')}/compensate", CompensationResult, kwargs or {})
