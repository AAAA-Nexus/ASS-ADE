# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a2_mo_composites/mo_draft_ratchetsession.py:7
# Component id: mo.source.a2_mo_composites.ratchetsession
from __future__ import annotations

__version__ = "0.1.0"

class RatchetSession(NexusModel):
    """/v1/ratchet/register"""
    session_id: str | None = None
    epoch: int | None = None
    next_rekey_at: int | None = None
    fips_203_compliant: bool | None = None
