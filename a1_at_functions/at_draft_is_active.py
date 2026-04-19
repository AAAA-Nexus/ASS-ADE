# Extracted from C:/!ass-ade/src/ass_ade/nexus/session.py:28
# Component id: at.source.ass_ade.is_active
from __future__ import annotations

__version__ = "0.1.0"

def is_active(self) -> bool:
    return self._started and self.session_id is not None
