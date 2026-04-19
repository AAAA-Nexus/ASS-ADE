# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a2_mo_composites/mo_draft_consensussession.py:7
# Component id: mo.source.a2_mo_composites.consensussession
from __future__ import annotations

__version__ = "0.1.0"

class ConsensusSession(NexusModel):
    """/v1/consensus/session — CSN-100"""
    session_id: str | None = None
    quorum_mode: str | None = None
    required_votes: int | None = None
    status: str | None = None
