# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a2_mo_composites/mo_draft_nexusclient.py:467
# Component id: mo.source.a2_mo_composites.swarm_relay
from __future__ import annotations

__version__ = "0.1.0"

def swarm_relay(self, from_id: str, to: str, message: dict, ttl: int = 3600, **kwargs: Any) -> SwarmRelayResult:
    """/v1/swarm/relay — A2A-ENT message relay across swarm. $0.008/call"""
    return self._post_model("/v1/swarm/relay", SwarmRelayResult, {"from": from_id, "to": to, "message": message, "ttl": ttl, **kwargs})
