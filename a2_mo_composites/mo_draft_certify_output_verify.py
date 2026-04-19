# Extracted from C:/!ass-ade/src/ass_ade/nexus/client.py:885
# Component id: mo.source.ass_ade.certify_output_verify
from __future__ import annotations

__version__ = "0.1.0"

def certify_output_verify(self, certificate_id: str) -> CertifiedOutput:
    """/v1/certify/output/{id}/verify — verify output certificate. $0.020/call"""
    return self._get_model(f"/v1/certify/output/{_pseg(certificate_id, 'certificate_id')}/verify", CertifiedOutput)
