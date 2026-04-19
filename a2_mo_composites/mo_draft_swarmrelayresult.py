# Extracted from C:/!ass-ade/.claude/worktrees/adoring-boyd-0e3a8f/src/ass_ade/nexus/models.py:411
# Component id: mo.source.ass_ade.swarmrelayresult
__version__ = "0.1.0"

class SwarmRelayResult(NexusModel):
    """/v1/swarm/relay and /v1/swarm/inbox"""
    delivered: bool | None = None
    message_id: str | None = None
    recipients: list[str] = Field(default_factory=list)
