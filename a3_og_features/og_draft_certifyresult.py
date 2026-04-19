# Extracted from C:/!ass-ade/src/ass_ade/workflows.py:47
# Component id: og.source.ass_ade.certifyresult
from __future__ import annotations

__version__ = "0.1.0"

class CertifyResult(BaseModel):
    text_preview: str
    hallucination_verdict: str | None = None
    ethics_verdict: str | None = None
    compliance_verdict: str | None = None
    certificate_id: str | None = None
    lineage_id: str | None = None
    passed: bool = False
