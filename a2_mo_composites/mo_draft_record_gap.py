# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a2_mo_composites/mo_draft_tcaengine.py:90
# Component id: mo.source.a2_mo_composites.record_gap
from __future__ import annotations

__version__ = "0.1.0"

def record_gap(self, description: str, source: str = "") -> None:
    """Record a documentation gap discovered during synthesis."""
    self._gaps.append(GAPEntry(description=description, source=source))
