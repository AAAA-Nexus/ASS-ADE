# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a2_mo_composites/mo_draft_nexusclient.py:527
# Component id: mo.source.a2_mo_composites.audit_log
from __future__ import annotations

__version__ = "0.1.0"

def audit_log(self, event: dict, **kwargs: Any) -> AuditLogEntry:
    """/v1/audit/log — tamper-evident event logging (GOV-103). $0.040/request"""
    return self._post_model("/v1/audit/log", AuditLogEntry, {"event": event, **kwargs})
