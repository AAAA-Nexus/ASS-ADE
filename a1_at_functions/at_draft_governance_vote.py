# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a1_at_functions/at_draft_governance_vote.py:7
# Component id: at.source.a1_at_functions.governance_vote
from __future__ import annotations

__version__ = "0.1.0"

def governance_vote(self, agent_id: str, proposal_id: str, vote: str, weight: float = 1.0, **kwargs: Any) -> GovernanceVote:
    """/v1/governance/vote — on-chain governance vote (GOV-112). $0.040/call"""
    return self._post_model("/v1/governance/vote", GovernanceVote, {
        "agent_id": agent_id, "proposal_id": proposal_id, "vote": vote, "weight": weight, **kwargs,
    })
