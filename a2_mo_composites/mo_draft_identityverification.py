# Extracted from C:/!ass-ade/src/ass_ade/nexus/models.py:238
# Component id: mo.source.ass_ade.identityverification
from __future__ import annotations

__version__ = "0.1.0"

class IdentityVerification(NexusModel):
    """/v1/identity/verify"""
    decision: str | None = None     # "allow" | "deny" | "flag"
    actor: str | None = None
    uniqueness_coefficient: float | None = None
    topology_proof: str | None = None
