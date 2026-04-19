# Extracted from C:/!ass-ade/src/ass_ade/nexus/models.py:58
# Component id: mo.source.ass_ade.agentcard
from __future__ import annotations

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
