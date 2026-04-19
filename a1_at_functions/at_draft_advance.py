# Extracted from C:/!ass-ade/src/ass_ade/nexus/session.py:46
# Component id: at.source.ass_ade.advance
from __future__ import annotations

__version__ = "0.1.0"

def advance(self) -> RatchetAdvance:
    """Advance the session epoch and re-key."""
    if not self.is_active:
        raise RuntimeError("No active session. Call start() first.")
    if self.session_id is None:
        raise RuntimeError("session_id must not be None")
    validate_session_id(self.session_id)
    result = self._client.ratchet_advance(self.session_id)
    self.epoch = result.new_epoch or self.epoch + 1
    return result
