# Extracted from C:/!ass-ade/src/ass_ade/nexus/client.py:722
# Component id: mo.source.ass_ade.audit_log
from __future__ import annotations

__version__ = "0.1.0"

def audit_log(self, event: dict, **kwargs: Any) -> AuditLogEntry:
    """/v1/audit/log — tamper-evident event logging (GOV-103). $0.040/request"""
    return self._post_model("/v1/audit/log", AuditLogEntry, {"event": event, **kwargs})
