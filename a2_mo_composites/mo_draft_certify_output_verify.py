# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a2_mo_composites/mo_draft_nexusclient.py:690
# Component id: mo.source.a2_mo_composites.certify_output_verify
from __future__ import annotations

__version__ = "0.1.0"

def certify_output_verify(self, certificate_id: str) -> CertifiedOutput:
    """/v1/certify/output/{id}/verify — verify output certificate. $0.020/call"""
    return self._get_model(f"/v1/certify/output/{_pseg(certificate_id, 'certificate_id')}/verify", CertifiedOutput)
