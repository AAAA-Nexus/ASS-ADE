# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a2_mo_composites/mo_draft_nexusclient.py:511
# Component id: mo.source.a2_mo_composites.security_pqc_sign
from __future__ import annotations

__version__ = "0.1.0"

def security_pqc_sign(self, data: str, **kwargs: Any) -> PqcSignResult:
    """/v1/security/pqc-sign — ML-DSA (Dilithium) post-quantum signatures. $0.020/request"""
    return self._post_model("/v1/security/pqc-sign", PqcSignResult, {"data": data, **kwargs})
