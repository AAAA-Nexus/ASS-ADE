# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a2_mo_composites/mo_draft_nexusclient.py:507
# Component id: mo.source.a2_mo_composites.security_shield
from __future__ import annotations

__version__ = "0.1.0"

def security_shield(self, payload: dict, **kwargs: Any) -> ShieldResult:
    """/v1/security/shield — payload sanitization layer for agentic tool calls. $0.040/request"""
    return self._post_model("/v1/security/shield", ShieldResult, {"payload": payload, **kwargs})
