# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a1_at_functions/at_draft_check_freshness.py:7
# Component id: at.source.a1_at_functions.check_freshness
from __future__ import annotations

__version__ = "0.1.0"

def check_freshness(self, path: str | Path) -> FreshnessReport:
    """Check whether a file is fresh (read within threshold)."""
    key = str(Path(path).resolve())
    ts = self._reads.get(key)
    now = time.time()
    if ts is None:
        return FreshnessReport(
            path=key, fresh=False, last_read_ts=None,
            age_hours=None, threshold_hours=self._threshold_hours,
        )
    age_hours = (now - ts) / 3600.0
    return FreshnessReport(
        path=key,
        fresh=age_hours <= self._threshold_hours,
        last_read_ts=ts,
        age_hours=round(age_hours, 2),
        threshold_hours=self._threshold_hours,
    )
