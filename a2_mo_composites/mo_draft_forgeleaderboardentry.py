# Extracted from C:/!ass-ade/.claude/worktrees/adoring-boyd-0e3a8f/src/ass_ade/nexus/models.py:1057
# Component id: mo.source.ass_ade.forgeleaderboardentry
__version__ = "0.1.0"

class ForgeLeaderboardEntry(NexusModel):
    agent_id: str | None = None
    name: str | None = None
    score: float | None = None
    rank: int | None = None
    badges: list[str] = Field(default_factory=list)
