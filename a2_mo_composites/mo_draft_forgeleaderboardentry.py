# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a2_mo_composites/mo_draft_forgeleaderboardentry.py:7
# Component id: mo.source.a2_mo_composites.forgeleaderboardentry
from __future__ import annotations

__version__ = "0.1.0"

class ForgeLeaderboardEntry(NexusModel):
    agent_id: str | None = None
    name: str | None = None
    score: float | None = None
    rank: int | None = None
    badges: list[str] = Field(default_factory=list)
