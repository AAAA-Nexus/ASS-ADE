# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a1_at_functions/at_draft_get_gaps.py:7
# Component id: at.source.a1_at_functions.get_gaps
from __future__ import annotations

__version__ = "0.1.0"

def get_gaps(self) -> list[dict[str, Any]]:
    return [
        {"description": g.description, "source": g.source, "ts": g.ts}
        for g in self._gaps
    ]
