# Extracted from C:/!ass-ade/src/ass_ade/nexus/models.py:460
# Component id: mo.source.ass_ade.shieldresult
from __future__ import annotations

__version__ = "0.1.0"

class ShieldResult(NexusModel):
    """/v1/security/shield"""
    sanitized: bool | None = None
    blocked: bool | None = None
    payload: dict | None = None
