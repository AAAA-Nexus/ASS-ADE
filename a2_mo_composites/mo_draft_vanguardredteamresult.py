# Extracted from C:/!ass-ade/.claude/worktrees/adoring-boyd-0e3a8f/src/ass_ade/nexus/models.py:1000
# Component id: mo.source.ass_ade.vanguardredteamresult
__version__ = "0.1.0"

class VanguardRedTeamResult(NexusModel):
    """POST /v1/vanguard/continuous-redteam"""
    run_id: str | None = None
    agent_id: str | None = None
    vulnerabilities_found: int | None = None
    severity: str | None = None
    findings: list[dict] = Field(default_factory=list)
    next_run_at: int | None = None
