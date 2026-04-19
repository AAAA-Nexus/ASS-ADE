# Extracted from C:/!ass-ade/.claude/worktrees/adoring-boyd-0e3a8f/src/ass_ade/nexus/models.py:1065
# Component id: mo.source.ass_ade.forgeleaderboardresponse
__version__ = "0.1.0"

class ForgeLeaderboardResponse(NexusModel):
    """GET /v1/forge/leaderboard"""
    entries: list[ForgeLeaderboardEntry] = Field(default_factory=list)
    epoch: int | None = None
