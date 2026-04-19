# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a3_og_features/og_draft_trustgateresult.py:7
# Component id: og.source.a3_og_features.trustgateresult
from __future__ import annotations

__version__ = "0.1.0"

class TrustGateResult(BaseModel):
    agent_id: str
    verdict: str  # ALLOW | DENY | WARN
    steps: list[TrustGateStep] = Field(default_factory=list)
    trust_score: float | None = None
    reputation_tier: str | None = None
