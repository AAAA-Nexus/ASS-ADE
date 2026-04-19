# Extracted from C:/!ass-ade/.claude/worktrees/beautiful-dubinsky-c2cb48/a2_mo_composites/mo_draft_agentcard.py:5
# Component id: mo.source.ass_ade.agentcard
__version__ = "0.1.0"

class AgentCard(NexusModel):
    name: str
    version: str | None = None
    capabilities: Any = None
    skills: list[AgentSkill] = Field(default_factory=list)
    trialPolicy: TrialPolicy | None = None
    authentication: AuthenticationInfo | None = None
    payment: dict | None = None
    endpoints: str | None = None
