# Extracted from C:/!ass-ade/src/ass_ade/nexus/client.py:460
# Component id: mo.source.ass_ade.ratchet_advance
from __future__ import annotations

__version__ = "0.1.0"

def ratchet_advance(self, session_id: str, **kwargs: Any) -> RatchetAdvance:
    """/v1/ratchet/advance — advance epoch + re-key. $0.008/call"""
    return self._post_model("/v1/ratchet/advance", RatchetAdvance, {"session_id": session_id, **kwargs})
