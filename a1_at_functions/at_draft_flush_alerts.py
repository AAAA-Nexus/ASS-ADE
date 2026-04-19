# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a1_at_functions/at_draft_flush_alerts.py:7
# Component id: at.source.a1_at_functions.flush_alerts
from __future__ import annotations

__version__ = "0.1.0"

def flush_alerts(self) -> list[Alert]:
    """Drain and return the unflushed alerts buffer."""
    drained = list(self._unflushed)
    self._unflushed.clear()
    return drained
