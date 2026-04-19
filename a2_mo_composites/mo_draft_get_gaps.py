# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a2_mo_composites/mo_draft_tcaengine.py:94
# Component id: mo.source.a2_mo_composites.get_gaps
from __future__ import annotations

__version__ = "0.1.0"

def get_gaps(self) -> list[dict[str, Any]]:
    return [
        {"description": g.description, "source": g.source, "ts": g.ts}
        for g in self._gaps
    ]
