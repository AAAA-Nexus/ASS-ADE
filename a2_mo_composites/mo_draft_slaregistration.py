# Extracted from C:/!ass-ade/src/ass_ade/nexus/models.py:309
# Component id: mo.source.ass_ade.slaregistration
from __future__ import annotations

__version__ = "0.1.0"

class SlaRegistration(NexusModel):
    """/v1/sla/register"""
    sla_id: str | None = None
    bond_usdc: float | None = None
    commitments: dict | None = None
