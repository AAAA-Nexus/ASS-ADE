# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a2_mo_composites/mo_draft_swarmrelayresult.py:7
# Component id: mo.source.a2_mo_composites.swarmrelayresult
from __future__ import annotations

__version__ = "0.1.0"

class SwarmRelayResult(NexusModel):
    """/v1/swarm/relay and /v1/swarm/inbox"""
    delivered: bool | None = None
    message_id: str | None = None
    recipients: list[str] = Field(default_factory=list)
