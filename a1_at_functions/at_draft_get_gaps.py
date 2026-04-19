# Extracted from C:/!ass-ade/src/ass_ade/agent/tca.py:129
# Component id: at.source.ass_ade.get_gaps
from __future__ import annotations

__version__ = "0.1.0"

def get_gaps(self) -> list[dict[str, Any]]:
    return [
        {"description": g.description, "source": g.source, "ts": g.ts}
        for g in self._gaps
    ]
