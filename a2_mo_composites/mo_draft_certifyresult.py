# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a2_mo_composites/mo_draft_certifyresult.py:7
# Component id: mo.source.a2_mo_composites.certifyresult
from __future__ import annotations

__version__ = "0.1.0"

class CertifyResult(NexusModel):
    ok: bool = False
    path: str | None = None
    valid: bool = False
    root_digest: str | None = None
    signature: str | None = None
    signed_by: str | None = None
    issued_at: str | None = None
    lora_captured: bool = False
    credit_used: float | None = None
    certificate: dict[str, Any] = {}
    message: str | None = None
