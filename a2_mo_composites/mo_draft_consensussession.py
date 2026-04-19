# Extracted from C:/!ass-ade/src/ass_ade/nexus/models.py:614
# Component id: mo.source.ass_ade.consensussession
from __future__ import annotations

__version__ = "0.1.0"

class ConsensusSession(NexusModel):
    """/v1/consensus/session — CSN-100"""
    session_id: str | None = None
    quorum_mode: str | None = None
    required_votes: int | None = None
    status: str | None = None
