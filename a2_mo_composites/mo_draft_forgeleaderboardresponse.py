# Extracted from C:/!ass-ade/src/ass_ade/nexus/models.py:1065
# Component id: mo.source.ass_ade.forgeleaderboardresponse
from __future__ import annotations

__version__ = "0.1.0"

class ForgeLeaderboardResponse(NexusModel):
    """GET /v1/forge/leaderboard"""
    entries: list[ForgeLeaderboardEntry] = Field(default_factory=list)
    epoch: int | None = None
