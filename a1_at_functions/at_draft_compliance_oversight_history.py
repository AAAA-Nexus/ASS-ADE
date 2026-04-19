# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a1_at_functions/at_draft_compliance_oversight_history.py:7
# Component id: at.source.a1_at_functions.compliance_oversight_history
from __future__ import annotations

__version__ = "0.1.0"

def compliance_oversight_history(self, system_id: str, **kwargs: Any) -> dict:
    """/v1/compliance/oversight/history — paginated signed history (OVS-101). $0.020/query"""
    return self._get_raw("/v1/compliance/oversight/history", system_id=system_id, **kwargs)
