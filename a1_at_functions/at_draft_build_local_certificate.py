# Extracted from C:/!ass-ade/src/ass_ade/local/certifier.py:75
# Component id: at.source.ass_ade.build_local_certificate
from __future__ import annotations

__version__ = "0.1.0"

def build_local_certificate(root: Path, version: str | None = None) -> dict[str, Any]:
    return {
        "schema": "ASS-ADE-CERT-001",
        "version": version or "unknown",
        "digest": compute_codebase_digest(root),
        "signed_by": None,
        "signature": None,
        "valid": False,
        "issuer": "atomadic.tech",
    }
