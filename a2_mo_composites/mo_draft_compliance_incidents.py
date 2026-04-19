# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a2_mo_composites/mo_draft_nexusclient.py:902
# Component id: mo.source.a2_mo_composites.compliance_incidents
from __future__ import annotations

__version__ = "0.1.0"

def compliance_incidents(self, system_id: str, **kwargs: Any) -> dict:
    """/v1/compliance/incidents — incident registry query (INC-101). $0.020/query"""
    return self._get_raw("/v1/compliance/incidents", system_id=system_id, **kwargs)
