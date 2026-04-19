# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a2_mo_composites/mo_draft_nexusclient.py:1152
# Component id: mo.source.a2_mo_composites.forge_leaderboard
from __future__ import annotations

__version__ = "0.1.0"

def forge_leaderboard(self, **kwargs: Any) -> ForgeLeaderboardResponse:
    """GET /v1/forge/leaderboard — Forge agent leaderboard. Free."""
    return self._get_model("/v1/forge/leaderboard", ForgeLeaderboardResponse, **kwargs)
