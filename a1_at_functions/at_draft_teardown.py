# Extracted from C:/!ass-ade/src/ass_ade/nexus/session.py:77
# Component id: at.source.ass_ade.teardown
from __future__ import annotations

__version__ = "0.1.0"

def teardown(self) -> None:
    """Mark the session as ended (client-side only)."""
    self.session_id = None
    self.epoch = 0
    self._started = False
