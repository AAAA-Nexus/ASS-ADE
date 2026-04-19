# Extracted from C:/!ass-ade/src/ass_ade/nexus/client.py:468
# Component id: mo.source.ass_ade.ratchet_status
from __future__ import annotations

__version__ = "0.1.0"

def ratchet_status(self, session_id: str) -> RatchetStatus:
    """/v1/ratchet/status/{id} — epoch + remaining calls. $0.004/call"""
    return self._get_model(f"/v1/ratchet/status/{_pseg(session_id, 'session_id')}", RatchetStatus)
