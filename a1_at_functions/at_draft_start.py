# Extracted from C:/!ass-ade/src/ass_ade/nexus/session.py:31
# Component id: at.source.ass_ade.start
from __future__ import annotations

__version__ = "0.1.0"

def start(self, agent_id: str) -> RatchetSession:
    """Register a new RatchetGate session."""
    validate_agent_id(agent_id)
    # RatchetGate expects agent_id as an int multiple of G_18 (324)
    # The server handles the constraint; we send the raw value
    result = self._client.ratchet_register(
        int(agent_id) if agent_id.isdigit() else (
            int.from_bytes(hashlib.sha256(agent_id.encode("utf-8")).digest()[:4], "big") & 0x7FFFFFFF
        )
    )
    self.session_id = result.session_id
    self.epoch = result.epoch or 0
    self._started = True
    return result
