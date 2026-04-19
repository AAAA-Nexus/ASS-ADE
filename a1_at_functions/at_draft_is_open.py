# Extracted from C:/!ass-ade/src/ass_ade/nexus/resilience.py:154
# Component id: at.source.ass_ade.is_open
from __future__ import annotations

__version__ = "0.1.0"

def is_open(self) -> bool:
    if self._open_since is None:
        return False
    if time.monotonic() - self._open_since >= self._recovery_s:
        return False  # half-open: allow a probe
    return True
