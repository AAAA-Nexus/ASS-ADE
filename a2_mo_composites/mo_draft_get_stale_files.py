# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a2_mo_composites/mo_draft_tcaengine.py:76
# Component id: mo.source.a2_mo_composites.get_stale_files
from __future__ import annotations

__version__ = "0.1.0"

def get_stale_files(self, paths: list[str | Path] | None = None) -> list[FreshnessReport]:
    """Return stale freshness reports for all tracked paths (or given subset)."""
    if paths is not None:
        targets = [str(Path(p).resolve()) for p in paths]
    else:
        targets = list(self._reads.keys())
    stale = []
    for p in targets:
        report = self.check_freshness(p)
        if not report.fresh:
            stale.append(report)
    self._stale_count = len(stale)
    return stale
