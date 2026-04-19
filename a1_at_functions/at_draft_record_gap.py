# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a1_at_functions/at_draft_record_gap.py:7
# Component id: at.source.a1_at_functions.record_gap
from __future__ import annotations

__version__ = "0.1.0"

def record_gap(self, description: str, source: str = "") -> None:
    """Record a documentation gap discovered during synthesis."""
    self._gaps.append(GAPEntry(description=description, source=source))
