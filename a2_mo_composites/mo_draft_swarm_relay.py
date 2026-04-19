# Extracted from C:/!ass-ade/src/ass_ade/nexus/client.py:662
# Component id: mo.source.ass_ade.swarm_relay
from __future__ import annotations

__version__ = "0.1.0"

def swarm_relay(self, from_id: str, to: str, message: dict, ttl: int = 3600, **kwargs: Any) -> SwarmRelayResult:
    """/v1/swarm/relay — A2A-ENT message relay across swarm. $0.008/call"""
    return self._post_model("/v1/swarm/relay", SwarmRelayResult, {"from": from_id, "to": to, "message": message, "ttl": ttl, **kwargs})
