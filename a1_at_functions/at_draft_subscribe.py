# Extracted from C:/!ass-ade/src/ass_ade/agent/bas.py:90
# Component id: at.source.ass_ade.subscribe
from __future__ import annotations

__version__ = "0.1.0"

def subscribe(self, callback: Callable[[Alert], None]) -> None:
    self._subscribers.append(callback)
