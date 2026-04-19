# Extracted from C:/!ass-ade/src/ass_ade/nexus/models.py:745
# Component id: sy.source.ass_ade.bridgeverify
from __future__ import annotations

__version__ = "0.1.0"

class BridgeVerify(NexusModel):
    """/v1/defi/bridge-verify — BRP-100"""
    safe: bool | None = None
    relay_reliability: float | None = None
    audit_score: float | None = None
    liquidity_depth_usdc: float | None = None
