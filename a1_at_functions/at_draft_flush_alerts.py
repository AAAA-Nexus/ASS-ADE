# Extracted from C:/!ass-ade/src/ass_ade/agent/bas.py:216
# Component id: at.source.ass_ade.flush_alerts
from __future__ import annotations

__version__ = "0.1.0"

def flush_alerts(self) -> list[Alert]:
    """Drain and return the unflushed alerts buffer."""
    drained = list(self._unflushed)
    self._unflushed.clear()
    return drained
