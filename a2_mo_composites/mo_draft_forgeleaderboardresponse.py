# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a2_mo_composites/mo_draft_forgeleaderboardresponse.py:7
# Component id: mo.source.a2_mo_composites.forgeleaderboardresponse
from __future__ import annotations

__version__ = "0.1.0"

class ForgeLeaderboardResponse(NexusModel):
    """GET /v1/forge/leaderboard"""
    entries: list[ForgeLeaderboardEntry] = Field(default_factory=list)
    epoch: int | None = None
