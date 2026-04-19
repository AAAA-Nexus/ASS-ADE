# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a2_mo_composites/mo_draft_nexusclient.py:497
# Component id: mo.source.a2_mo_composites.security_zero_day
from __future__ import annotations

__version__ = "0.1.0"

def security_zero_day(self, payload: dict, **kwargs: Any) -> ZeroDayResult:
    """/v1/security/zero-day — zero-day pattern detector for agent payloads. $0.040/request"""
    return self._post_model("/v1/security/zero-day", ZeroDayResult, {"payload": payload, **kwargs})
