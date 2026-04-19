# Extracted from C:/!ass-ade/src/ass_ade/nexus/client.py:456
# Component id: mo.source.ass_ade.ratchet_register
from __future__ import annotations

__version__ = "0.1.0"

def ratchet_register(self, agent_id: int, **kwargs: Any) -> RatchetSession:
    """/v1/ratchet/register — new session with epoch counter. agent_id must be a multiple of G_18 (324). $0.008/call"""
    return self._post_model("/v1/ratchet/register", RatchetSession, {"agent_id": agent_id, **kwargs})
