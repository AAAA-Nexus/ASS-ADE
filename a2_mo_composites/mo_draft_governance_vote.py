# Extracted from C:/!ass-ade/src/ass_ade/nexus/client.py:1165
# Component id: mo.source.ass_ade.governance_vote
from __future__ import annotations

__version__ = "0.1.0"

def governance_vote(self, agent_id: str, proposal_id: str, vote: str, weight: float = 1.0, **kwargs: Any) -> GovernanceVote:
    """/v1/governance/vote — on-chain governance vote (GOV-112). $0.040/call"""
    return self._post_model("/v1/governance/vote", GovernanceVote, {
        "agent_id": agent_id, "proposal_id": proposal_id, "vote": vote, "weight": weight, **kwargs,
    })
