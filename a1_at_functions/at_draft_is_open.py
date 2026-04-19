# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a1_at_functions/at_draft_is_open.py:7
# Component id: at.source.a1_at_functions.is_open
from __future__ import annotations

__version__ = "0.1.0"

def is_open(self) -> bool:
    if self._open_since is None:
        return False
    if time.monotonic() - self._open_since >= self._recovery_s:
        return False  # half-open: allow a probe
    return True
