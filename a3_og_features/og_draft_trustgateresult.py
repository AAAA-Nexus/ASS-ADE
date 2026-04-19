# Extracted from C:/!ass-ade/.claude/worktrees/adoring-boyd-0e3a8f/src/ass_ade/workflows.py:39
# Component id: og.source.ass_ade.trustgateresult
__version__ = "0.1.0"

class TrustGateResult(BaseModel):
    agent_id: str
    verdict: str  # ALLOW | DENY | WARN
    steps: list[TrustGateStep] = Field(default_factory=list)
    trust_score: float | None = None
    reputation_tier: str | None = None
