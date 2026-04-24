"""Hero workflows — multi-step orchestrated flows over AAAA-Nexus.

These workflows compose multiple NexusClient calls into opinionated,
production-grade pipelines. Each workflow:

  - Validates all inputs before any network call
  - Returns a typed result model
  - Works in hybrid and premium profiles
  - Keeps all proprietary logic server-side
"""

from __future__ import annotations

import logging
from typing import Any

import httpx
from pydantic import BaseModel, Field

from ass_ade.nexus.client import NexusClient
from ass_ade.nexus.errors import NexusError
from ass_ade.nexus.validation import validate_agent_id, validate_prompt

_LOG = logging.getLogger(__name__)
_WORKFLOW_ERRORS = (NexusError, httpx.HTTPError, OSError, RuntimeError, ValueError)

# ══════════════════════════════════════════════════════════════════════════════
# Result models
# ══════════════════════════════════════════════════════════════════════════════


class TrustGateStep(BaseModel):
    name: str
    passed: bool
    detail: str = ""
    raw: dict[str, Any] = Field(default_factory=dict)


class TrustGateResult(BaseModel):
    agent_id: str
    verdict: str  # ALLOW | DENY | WARN
    steps: list[TrustGateStep] = Field(default_factory=list)
    trust_score: float | None = None
    reputation_tier: str | None = None


class CertifyResult(BaseModel):
    text_preview: str
    hallucination_verdict: str | None = None
    ethics_verdict: str | None = None
    compliance_verdict: str | None = None
    certificate_id: str | None = None
    lineage_id: str | None = None
    passed: bool = False


class SafeExecuteResult(BaseModel):
    tool_name: str | None = None
    shield_passed: bool = False
    prompt_scan_passed: bool = False
    invocation_result: dict[str, Any] = Field(default_factory=dict)
    certificate_id: str | None = None


# ══════════════════════════════════════════════════════════════════════════════
# Workflow: Trust Gate
# ══════════════════════════════════════════════════════════════════════════════


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


# ══════════════════════════════════════════════════════════════════════════════
# Workflow: Output Certification
# ══════════════════════════════════════════════════════════════════════════════


def certify_output(client: NexusClient, text: str) -> CertifyResult:
    """Multi-step output certification: hallucination → ethics → compliance → certify → lineage.

    Returns a certificate ID that can be verified later.
    """
    text = validate_prompt(text)
    result = CertifyResult(text_preview=text[:120])

    # Step 1: Hallucination oracle
    try:
        hall = client.hallucination_oracle(text)
        result.hallucination_verdict = getattr(hall, "verdict", None)
    except _WORKFLOW_ERRORS:
        _LOG.warning("Hallucination oracle failed during certification", exc_info=True)
        result.hallucination_verdict = "error"

    # Step 2: Ethics check
    try:
        eth = client.ethics_check(text)
        eth_raw = eth.model_dump() if hasattr(eth, "model_dump") else {}
        result.ethics_verdict = "safe" if eth_raw.get("safe") else str(eth_raw.get("safe", "unknown"))
    except _WORKFLOW_ERRORS:
        _LOG.warning("Ethics check failed during certification", exc_info=True)
        result.ethics_verdict = "error"

    # Step 3: Compliance check
    try:
        comp = client.compliance_check(text)
        comp_raw = comp.model_dump() if hasattr(comp, "model_dump") else {}
        result.compliance_verdict = "compliant" if comp_raw.get("compliant") else str(comp_raw.get("compliant", "unknown"))
    except _WORKFLOW_ERRORS:
        _LOG.warning("Compliance check failed during certification", exc_info=True)
        result.compliance_verdict = "error"

    # Step 4: Certify output via AAAA-Nexus
    try:
        cert = client.certify_output(text, rubric=["accuracy", "safety", "compliance"])
        cert_raw = cert.model_dump() if hasattr(cert, "model_dump") else {}
        result.certificate_id = cert_raw.get("certificate_id")
    except _WORKFLOW_ERRORS:
        _LOG.warning("Output certification failed", exc_info=True)
        result.certificate_id = None

    # Step 5: Lineage record
    try:
        lin = client.lineage_record(
            intent="output_certification",
            constraints=["hallucination_check", "ethics_check", "compliance_check"],
            outcome=f"certificate={result.certificate_id or 'none'}",
        )
        lin_raw = lin.model_dump() if hasattr(lin, "model_dump") else {}
        result.lineage_id = lin_raw.get("record_id")
    except _WORKFLOW_ERRORS:
        _LOG.warning("Lineage recording failed during certification", exc_info=True)
        result.lineage_id = None

    result.passed = (
        result.hallucination_verdict not in (None, "error", "unsafe")
        and result.ethics_verdict not in (None, "error")
        and result.certificate_id is not None
    )

    return result


# ══════════════════════════════════════════════════════════════════════════════
# Workflow: Safe Execute (MCP tool with AEGIS wrapping)
# ══════════════════════════════════════════════════════════════════════════════


def safe_execute(
    client: NexusClient,
    tool_name: str,
    tool_input: str = "",
    *,
    agent_id: str | None = None,
) -> SafeExecuteResult:
    """AEGIS-wrapped MCP tool execution: shield → scan → proxy → certify.

    Uses the AEGIS MCP proxy for firewalled execution rather than direct invocation.
    """
    result = SafeExecuteResult(tool_name=tool_name)

    # Step 1: Security shield — sanitise payload
    try:
        shield = client.security_shield({"tool": tool_name, "input": tool_input})
        shield_raw = shield.model_dump() if hasattr(shield, "model_dump") else {}
        result.shield_passed = not shield_raw.get("blocked", False)
    except _WORKFLOW_ERRORS:
        _LOG.warning("Security shield failed for tool=%s", tool_name, exc_info=True)
        result.shield_passed = False

    # Step 2: Prompt injection scan
    if tool_input:
        try:
            scan = client.prompt_inject_scan(tool_input)
            scan_raw = scan.model_dump() if hasattr(scan, "model_dump") else {}
            result.prompt_scan_passed = not scan_raw.get("threat_detected", False)
        except _WORKFLOW_ERRORS:
            _LOG.warning("Prompt scan failed for tool=%s", tool_name, exc_info=True)
            result.prompt_scan_passed = False
    else:
        result.prompt_scan_passed = True

    # Step 3: AEGIS MCP proxy execute
    try:
        proxy_result = client.aegis_mcp_proxy(
            tool=tool_name,
            tool_input=tool_input,
            agent_id=agent_id,
        )
        result.invocation_result = proxy_result.model_dump() if hasattr(proxy_result, "model_dump") else {}
    except _WORKFLOW_ERRORS:
        _LOG.warning(
            "AEGIS MCP proxy failed for tool=%s, agent_id=%s",
            tool_name,
            agent_id,
            exc_info=True,
        )
        result.invocation_result = {"error": "proxy_failed"}

    # Step 4: Optional output certification
    output_text = str(result.invocation_result.get("tool_result", result.invocation_result.get("allowed", "")))
    if output_text and result.shield_passed and result.prompt_scan_passed:
        try:
            cert = client.certify_output(output_text, rubric=["tool_safety", "output_integrity"])
            cert_raw = cert.model_dump() if hasattr(cert, "model_dump") else {}
            result.certificate_id = cert_raw.get("certificate_id")
        except _WORKFLOW_ERRORS:
            _LOG.warning("Output certification failed for tool=%s", tool_name, exc_info=True)

    return result
