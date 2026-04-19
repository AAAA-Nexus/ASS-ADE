# Extracted from C:/!ass-ade/src/ass_ade/nexus/models.py:161
# Component id: mo.source.ass_ade.ratchetsession
from __future__ import annotations

__version__ = "0.1.0"

class RatchetSession(NexusModel):
    """/v1/ratchet/register"""
    session_id: str | None = None
    epoch: int | None = None
    next_rekey_at: int | None = None
    fips_203_compliant: bool | None = None
