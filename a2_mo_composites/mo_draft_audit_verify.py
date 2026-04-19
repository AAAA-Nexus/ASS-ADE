# Extracted from C:/!ass-ade/src/ass_ade/nexus/client.py:726
# Component id: mo.source.ass_ade.audit_verify
from __future__ import annotations

__version__ = "0.1.0"

def audit_verify(self, **kwargs: Any) -> AuditVerifyResult:
    """/v1/audit/verify — verify audit trail integrity. $0.040/request"""
    return self._post_model("/v1/audit/verify", AuditVerifyResult, kwargs or {})
