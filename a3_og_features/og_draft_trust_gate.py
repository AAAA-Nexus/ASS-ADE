# Extracted from C:/!ass-ade/src/ass_ade/workflows.py:70
# Component id: og.source.ass_ade.trust_gate
from __future__ import annotations

__version__ = "0.1.0"

def trust_gate(client: NexusClient, agent_id: str) -> TrustGateResult:
    """Multi-step agent trust gating: identity → sybil → trust → reputation → gate decision.

    Gate logic (public-safe, deterministic):
      - identity fail   → DENY
      - sybil detected  → DENY
      - trust < 0.5     → DENY
      - trust < 0.7 and reputation not in {gold, platinum} → WARN
      - otherwise       → ALLOW
    """
    agent_id = validate_agent_id(agent_id)
    steps: list[TrustGateStep] = []
    verdict = "ALLOW"

    # Step 1: Identity verification
    try:
        id_result = client.identity_verify(agent_id)
        id_raw = id_result.model_dump() if hasattr(id_result, "model_dump") else {}
        decision = id_raw.get("decision", "allow")
        id_passed = decision != "deny"
        steps.append(TrustGateStep(name="identity_verify", passed=id_passed, detail=f"decision={decision}", raw=id_raw))
        if not id_passed:
            verdict = "DENY"
    except _WORKFLOW_ERRORS:
        _LOG.warning("Identity verification failed for agent_id=%s", agent_id, exc_info=True)
        steps.append(TrustGateStep(name="identity_verify", passed=False, detail="step_failed"))
        verdict = "DENY"

    # Step 2: Sybil check
    try:
        sybil_result = client.sybil_check(agent_id)
        sybil_raw = sybil_result.model_dump() if hasattr(sybil_result, "model_dump") else {}
        sybil_risk = sybil_raw.get("sybil_risk", "low")
        sybil_ok = sybil_risk != "high"
        steps.append(TrustGateStep(name="sybil_check", passed=sybil_ok, detail=f"sybil_risk={sybil_risk}", raw=sybil_raw))
        if not sybil_ok:
            verdict = "DENY"
    except _WORKFLOW_ERRORS:
        _LOG.warning("Sybil check failed for agent_id=%s", agent_id, exc_info=True)
        steps.append(TrustGateStep(name="sybil_check", passed=False, detail="step_failed"))

    # Step 3: Trust score
    trust_score_val: float | None = None
    try:
        trust_result = client.trust_score(agent_id)
        trust_raw = trust_result.model_dump() if hasattr(trust_result, "model_dump") else {}
        trust_score_val = trust_raw.get("score")
        score_ok = trust_score_val is not None and trust_score_val >= 0.5
        steps.append(TrustGateStep(
            name="trust_score", passed=score_ok,
            detail=f"score={trust_score_val}, tier={trust_raw.get('tier', 'unknown')}",
            raw=trust_raw,
        ))
        if trust_score_val is not None and trust_score_val < 0.5:
            verdict = "DENY"
    except _WORKFLOW_ERRORS:
        _LOG.warning("Trust score check failed for agent_id=%s", agent_id, exc_info=True)
        steps.append(TrustGateStep(name="trust_score", passed=False, detail="step_failed"))

    # Step 4: Reputation score
    reputation_tier: str | None = None
    try:
        rep_result = client.reputation_score(agent_id)
        rep_raw = rep_result.model_dump() if hasattr(rep_result, "model_dump") else {}
        reputation_tier = rep_raw.get("tier")
        rep_ok = reputation_tier is not None
        steps.append(TrustGateStep(
            name="reputation_score", passed=rep_ok,
            detail=f"tier={reputation_tier}, fee_multiplier={rep_raw.get('fee_multiplier', 'n/a')}",
            raw=rep_raw,
        ))
    except _WORKFLOW_ERRORS:
        _LOG.warning("Reputation score check failed for agent_id=%s", agent_id, exc_info=True)
        steps.append(TrustGateStep(name="reputation_score", passed=False, detail="step_failed"))

    # Step 5: Gate decision
    if verdict == "ALLOW" and trust_score_val is not None and trust_score_val < 0.7:
        if reputation_tier not in {"gold", "platinum"}:
            verdict = "WARN"

    return TrustGateResult(
        agent_id=agent_id,
        verdict=verdict,
        steps=steps,
        trust_score=trust_score_val,
        reputation_tier=reputation_tier,
    )
