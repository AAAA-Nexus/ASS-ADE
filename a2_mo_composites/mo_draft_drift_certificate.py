# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a2_mo_composites/mo_draft_nexusclient.py:927
# Component id: mo.source.a2_mo_composites.drift_certificate
from __future__ import annotations

__version__ = "0.1.0"

def drift_certificate(self, check_id: str | None = None, *, model_id: str | None = None) -> DriftCertificate:
    """/v1/drift/certificate — signed drift compliance cert (DRG-101). $0.010/cert"""
    return self._get_model("/v1/drift/certificate", DriftCertificate, check_id=check_id or model_id or "")
