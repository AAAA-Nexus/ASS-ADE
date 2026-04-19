# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a2_mo_composites/mo_draft_tcaengine.py:114
# Component id: mo.source.a2_mo_composites.report
from __future__ import annotations

__version__ = "0.1.0"

def report(self) -> dict[str, Any]:
    return {
        "engine": "tca",
        "tracked_files": len(self._reads),
        "stale_count": self._stale_count,
        "gap_count": len(self._gaps),
        "threshold_hours": self._threshold_hours,
    }
