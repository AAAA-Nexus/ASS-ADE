# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a2_mo_composites/mo_draft_freshnessreport.py:7
# Component id: mo.source.a2_mo_composites.freshnessreport
from __future__ import annotations

__version__ = "0.1.0"

class FreshnessReport:
    path: str
    fresh: bool
    last_read_ts: float | None
    age_hours: float | None
    threshold_hours: float
