# Extracted from C:/!ass-ade/src/ass_ade/nexus/client.py:1076
# Component id: mo.source.ass_ade.compliance_oversight_history
from __future__ import annotations

__version__ = "0.1.0"

def compliance_oversight_history(self, system_id: str, **kwargs: Any) -> dict:
    """/v1/compliance/oversight/history — paginated signed history (OVS-101). $0.020/query"""
    return self._get_raw("/v1/compliance/oversight/history", system_id=system_id, **kwargs)
