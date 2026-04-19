# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a3_og_features/og_draft_certifyresult.py:7
# Component id: og.source.a3_og_features.certifyresult
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
