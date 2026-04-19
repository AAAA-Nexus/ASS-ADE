# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a1_at_functions/at_draft_subscribe.py:7
# Component id: at.source.a1_at_functions.subscribe
from __future__ import annotations

__version__ = "0.1.0"

def subscribe(self, callback: Callable[[Alert], None]) -> None:
    self._subscribers.append(callback)
