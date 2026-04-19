# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a2_mo_composites/mo_draft_pqcsignresult.py:7
# Component id: mo.source.a2_mo_composites.pqcsignresult
from __future__ import annotations

__version__ = "0.1.0"

class PqcSignResult(NexusModel):
    """/v1/security/pqc-sign"""
    signature: str | None = None
    algorithm: str | None = None   # "ML-DSA (Dilithium)"
    public_key: str | None = None
