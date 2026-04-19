# Extracted from C:/!ass-ade/src/ass_ade/agent/tca.py:135
# Component id: at.source.ass_ade.pre_synthesis_check
from __future__ import annotations

__version__ = "0.1.0"

def pre_synthesis_check(self, candidate_paths: list[str]) -> dict[str, Any]:
    """Run freshness check for a list of candidate write targets.

    Returns dict with: fresh_count, stale_paths, ncb_violated, gaps
    """
    stale = self.get_stale_files([p for p in candidate_paths if p])
    stale_paths = [r.path for r in stale]
    return {
        "fresh_count": len(candidate_paths) - len(stale_paths),
        "stale_paths": stale_paths,
        "ncb_violated": len(stale_paths) > 0,
        "gaps": self.get_gaps(),
    }
