# Extracted from C:/!ass-ade/src/ass_ade/nexus/models.py:784
# Component id: qk.source.ass_ade.lineageproof
from __future__ import annotations

__version__ = "0.1.0"

class LineageProof(NexusModel):
    """/v1/compliance/lineage — LIN-100"""
    chain_hash: str | None = None
    stages: int | None = None
    integrity_ok: bool | None = None
