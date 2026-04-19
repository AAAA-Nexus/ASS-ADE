# Extracted from C:/!ass-ade/src/ass_ade/nexus/resilience.py:127
# Component id: at.source.ass_ade.close
from __future__ import annotations

__version__ = "0.1.0"

def close(self) -> None:
    self._wrapped.close()
