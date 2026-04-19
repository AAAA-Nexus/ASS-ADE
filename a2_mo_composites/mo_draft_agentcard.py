# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a2_mo_composites/mo_draft_agentcard.py:7
# Component id: mo.source.a2_mo_composites.agentcard
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
