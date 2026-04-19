# Extracted from C:/!ass-ade/src/ass_ade/agent/tca.py:125
# Component id: at.source.ass_ade.record_gap
from __future__ import annotations

__version__ = "0.1.0"

def record_gap(self, description: str, source: str = "") -> None:
    """Record a documentation gap discovered during synthesis."""
    self._gaps.append(GAPEntry(description=description, source=source))
