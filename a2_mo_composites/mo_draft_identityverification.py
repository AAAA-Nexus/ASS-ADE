# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a2_mo_composites/mo_draft_identityverification.py:7
# Component id: mo.source.a2_mo_composites.identityverification
from __future__ import annotations

__version__ = "0.1.0"

class IdentityVerification(NexusModel):
    """/v1/identity/verify"""
    decision: str | None = None     # "allow" | "deny" | "flag"
    actor: str | None = None
    uniqueness_coefficient: float | None = None
    topology_proof: str | None = None
