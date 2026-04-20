"""Pydantic response models for all AAAA-Nexus API product families.

Every model uses ``extra="allow"`` so forward-compatible with API additions.
Key fields are typed; everything else flows through the extra dict.

Product families covered (119+ endpoints):
  Discovery & Protocol · AI Inference · Hallucination / Trust Oracles
  RatchetGate · VeriRand · VeriDelegate · Agent Escrow · Reputation
  SLA Engine · Agent Discovery · Agent Swarm & Routing
  Prompt Intelligence · Security & Compliance (AEGIS)
  Control Plane (OAP/SPG/DLV/BCV/AIF/CSN/QTA/OCN/RBK/MFN)
  Trust Oracle · DeFi Suite · Compliance Products · VRF Gaming
  Text AI · Data Tools · Developer Tools · Governance · Billing
"""
from __future__ import annotations

from typing import Any

from pydantic import BaseModel, ConfigDict, Field


class NexusModel(BaseModel):
    model_config = ConfigDict(extra="allow")


# ── Discovery / Protocol ──────────────────────────────────────────────────────

class HealthStatus(NexusModel):
    status: str
    version: str | None = None
    build: str | None = None
    epoch: int | None = None


class OpenApiInfo(NexusModel):
    title: str | None = None
    version: str | None = None


class OpenApiDocument(NexusModel):
    openapi: str | None = None
    info: OpenApiInfo


class TrialPolicy(NexusModel):
    note: str | None = None


class AuthenticationInfo(NexusModel):
    trialAccess: str | None = None


class AgentSkill(NexusModel):
    id: str | None = None
    name: str | None = None


class AgentCard(NexusModel):
    name: str
    version: str | None = None
    capabilities: Any = None
    skills: list[AgentSkill] = Field(default_factory=list)
    trialPolicy: TrialPolicy | None = None
    authentication: AuthenticationInfo | None = None
    payment: dict | None = None
    endpoints: str | None = None


class PricingManifest(NexusModel):
    """/.well-known/pricing.json"""
    tiers: Any = None


class PlatformMetrics(NexusModel):
    """/v1/metrics"""
    request_volume: int | None = None
    p50_ms: float | None = None
    p99_ms: float | None = None


# ── MCP manifest (existing, kept for compat) ─────────────────────────────────

class CostEstimate(NexusModel):
    currency: str = "USDC"
    unit_cost: float | None = None
    rate_limit_rpm: int | None = None
    rate_limit_tpm: int | None = None
    notes: str | None = None


class MCPTool(NexusModel):
    name: str | None = None
    endpoint: str | None = None
    method: str | None = None
    paid: bool | None = None
    inputSchema: dict | None = Field(default=None)
    cost: CostEstimate | None = None


class MCPManifest(NexusModel):
    name: str
    version: str | None = None
    mcpVersion: str | None = None
    serverUrl: str | None = None
    tools: list[MCPTool] = Field(default_factory=list)


# ── AI Inference ──────────────────────────────────────────────────────────────

class InferenceResponse(NexusModel):
    """/v1/inference and /v1/embed"""
    result: str | None = None
    text: str | None = None          # alias used by some versions
    tokens_used: int | None = None
    model: str | None = None
    latency_ms: float | None = None
    helix_metadata: dict | None = None


class EmbedResponse(NexusModel):
    """/v1/embed — HELIX compressed embedding"""
    embedding: list[float] | None = Field(default=None)
    compressed: str | None = None    # base64 HELIX blob
    dimensions: int | None = None
    latency_ms: float | None = None


# ── Hallucination / Trust Oracles ─────────────────────────────────────────────

class HallucinationResult(NexusModel):
    """/v1/oracle/hallucination"""
    policy_epsilon: float | None = None
    verdict: str | None = None       # "safe" | "caution" | "unsafe"
    ceiling: str | None = None       # "proved-not-estimated"
    confidence: float | None = None


class TrustPhaseResult(NexusModel):
    """/v1/oracle/v-ai - geometric trust phase oracle response envelope."""
    phase: float | None = None
    certified: bool | None = None
    monotonicity_preserved: bool | None = None


class EntropyResult(NexusModel):
    """/v1/oracle/entropy"""
    entropy_bits: float | None = None
    epoch: int | None = None
    verdict: str | None = None


class TrustDecayResult(NexusModel):
    """/v1/trust/decay"""
    decayed_score: float | None = None
    original_score: float | None = None
    epochs_elapsed: int | None = None


# ── RatchetGate ───────────────────────────────────────────────────────────────

class RatchetSession(NexusModel):
    """/v1/ratchet/register"""
    session_id: str | None = None
    epoch: int | None = None
    next_rekey_at: int | None = None
    fips_203_compliant: bool | None = None


class RatchetAdvance(NexusModel):
    """/v1/ratchet/advance"""
    session_id: str | None = None
    new_epoch: int | None = None
    proof_token: str | None = None
    credential_age_bound_s: int | None = None


class RatchetProbeResult(NexusModel):
    """/v1/ratchet/probe — batch health check"""
    results: list[dict] = Field(default_factory=list)


class RatchetStatus(NexusModel):
    """/v1/ratchet/status/{id}"""
    session_id: str | None = None
    epoch: int | None = None
    remaining_calls: int | None = None
    status: str | None = None


# ── VeriRand / VRF ────────────────────────────────────────────────────────────

class RngResult(NexusModel):
    """/v1/rng/quantum"""
    numbers: list[float] = Field(default_factory=list)
    seed_ts: str | None = None
    proof: str | None = None
    verified: bool | None = None


class VrfDraw(NexusModel):
    """/v1/vrf/draw"""
    draw_id: str | None = None
    numbers: list[int] = Field(default_factory=list)
    proof: str | None = None
    range_min: int | None = None
    range_max: int | None = None


class VrfVerify(NexusModel):
    """/v1/vrf/verify-draw"""
    valid: bool | None = None
    draw_id: str | None = None
    proof: str | None = None


# ── VeriDelegate ──────────────────────────────────────────────────────────────

class DelegationValidation(NexusModel):
    """/v1/identity/delegation/validate and /v1/delegate/verify"""
    valid: bool | None = None
    depth: int | None = None
    depth_limit: int | None = None   # resolved from the oracle's `AN-TH-DEPTH-LIMIT` invariant
    receipt_id: str | None = None
    capability_attenuated: bool | None = None
    trust_vector: dict | None = None


class DelegateReceipt(NexusModel):
    """/v1/delegate/receipt/{id}"""
    receipt_id: str | None = None
    chain_hash: str | None = None
    issued_at: str | None = None
    payload: dict | None = None


# ── Identity & Auth ───────────────────────────────────────────────────────────

class IdentityVerification(NexusModel):
    """/v1/identity/verify"""
    decision: str | None = None     # "allow" | "deny" | "flag"
    actor: str | None = None
    uniqueness_coefficient: float | None = None
    topology_proof: str | None = None


class SybilCheckResult(NexusModel):
    """/v1/identity/sybil-check"""
    sybil_risk: str | None = None   # "low" | "medium" | "high"
    score: float | None = None
    flags: list[str] = Field(default_factory=list)


class ZeroTrustResult(NexusModel):
    """/v1/auth/zero-trust"""
    allowed: bool | None = None
    trust_level: str | None = None
    reason: str | None = None


# ── Agent Escrow ──────────────────────────────────────────────────────────────

class EscrowCreated(NexusModel):
    """/v1/escrow/create"""
    escrow_id: str | None = None
    amount_usdc: float | None = None
    status: str | None = None
    release_conditions: list[str] = Field(default_factory=list)
    expires_at: str | None = None


class EscrowStatus(NexusModel):
    """/v1/escrow/status/{id}"""
    escrow_id: str | None = None
    status: str | None = None   # "funded" | "released" | "disputed" | "resolved"
    amount_usdc: float | None = None


class EscrowResult(NexusModel):
    """Generic for release / dispute / arbitrate"""
    escrow_id: str | None = None
    status: str | None = None
    message: str | None = None


# ── Reputation Ledger ─────────────────────────────────────────────────────────

class ReputationScore(NexusModel):
    """/v1/reputation/score/{id}"""
    agent_id: str | None = None
    score: float | None = None
    tier: str | None = None    # "platinum" | "gold" | "silver" | "bronze" | "untrusted"
    fee_multiplier: float | None = None


class ReputationHistory(NexusModel):
    """/v1/reputation/history/{id}"""
    agent_id: str | None = None
    entries: list[dict] = Field(default_factory=list)


class ReputationRecord(NexusModel):
    """/v1/reputation/record"""
    recorded: bool | None = None
    entry_id: str | None = None


# ── SLA Engine ────────────────────────────────────────────────────────────────

class SlaRegistration(NexusModel):
    """/v1/sla/register"""
    sla_id: str | None = None
    bond_usdc: float | None = None
    commitments: dict | None = None


class SlaStatus(NexusModel):
    """/v1/sla/status/{id}"""
    sla_id: str | None = None
    compliance_score: float | None = None
    breach_count: int | None = None
    bond_remaining_usdc: float | None = None


class SlaResult(NexusModel):
    """Generic for report/breach"""
    sla_id: str | None = None
    compliant: bool | None = None
    penalty_usdc: float | None = None
    message: str | None = None


# ── Agent Discovery ───────────────────────────────────────────────────────────

class DiscoveredAgent(NexusModel):
    agent_id: Any = None
    name: str | None = None
    capabilities: Any = None
    reputation_score: float | None = None
    endpoint: str | None = None
    match_score: float | None = None


class DiscoveryResult(NexusModel):
    """/v1/discovery/search and /v1/discovery/recommend"""
    agents: list[DiscoveredAgent] = Field(default_factory=list)
    total: int | None = None
    query: Any = None


class AgentRegistry(NexusModel):
    """/v1/discovery/registry"""
    agents: list[DiscoveredAgent] = Field(default_factory=list)
    total_registered: int | None = None


# ── Agent Swarm & Routing ─────────────────────────────────────────────────────

class AgentRegistration(NexusModel):
    """/v1/agents/register"""
    agent_id: Any = None
    registered: Any = None


class AgentTopology(NexusModel):
    """/v1/agents/topology"""
    node_count: int | None = None
    edge_count: int | None = None
    topology: Any = None


class SemanticDiff(NexusModel):
    """/v1/agents/semantic-diff"""
    drift_score: float | None = None
    jaccard_similarity: float | None = None
    changed_concepts: list[str] = Field(default_factory=list)


class IntentClassification(NexusModel):
    """/v1/agents/intent-classify"""
    top_intents: list[dict] = Field(default_factory=list)   # [{intent, confidence}]
    primary_intent: str | None = None


class TokenBudget(NexusModel):
    """/v1/agents/token-budget"""
    estimates: dict | None = None   # model→cost
    recommended_model: str | None = None
    total_tokens: int | None = None


class ContradictionResult(NexusModel):
    """/v1/agents/contradiction"""
    contradicts: bool | None = None
    confidence: float | None = None
    explanation: str | None = None


class AgentPlan(NexusModel):
    """/v1/agents/plan"""
    steps: list[dict] = Field(default_factory=list)
    goal: str | None = None
    estimated_cost_usdc: float | None = None


class CapabilityMatch(NexusModel):
    """/v1/agents/capabilities/match"""
    matches: list[DiscoveredAgent] = Field(default_factory=list)
    task: str | None = None


class SwarmRelayResult(NexusModel):
    """/v1/swarm/relay and /v1/swarm/inbox"""
    delivered: bool | None = None
    message_id: str | None = None
    recipients: list[str] = Field(default_factory=list)


# ── Prompt Intelligence & Ethics ──────────────────────────────────────────────

class PromptScanResult(NexusModel):
    """/v1/prompts/inject-scan and /v1/security/prompt-scan"""
    threat_detected: bool | None = None
    threat_level: str | None = None  # "none" | "low" | "medium" | "high"
    confidence: float | None = None
    threat_report: dict | None = None


class PromptOptimized(NexusModel):
    """/v1/prompts/optimize"""
    original_tokens: int | None = None
    optimized_tokens: int | None = None
    optimized_prompt: str | None = None
    savings_pct: float | None = None


class EthicsCheckResult(NexusModel):
    """/v1/ethics/check and /v1/ethics/compliance"""
    safe: bool | None = None
    score: float | None = None
    axiom_bound: float | None = None
    violations: list[str] = Field(default_factory=list)


class ZeroDayResult(NexusModel):
    """/v1/security/zero-day"""
    vulnerable: bool | None = None
    patterns_matched: list[str] = Field(default_factory=list)
    severity: str | None = None


# ── Security & Compliance ─────────────────────────────────────────────────────

class ThreatScore(NexusModel):
    """/v1/threat/score"""
    threat_level: str | None = None   # "low" | "medium" | "high" | "critical"
    score: float | None = None
    vectors: dict | None = None       # velocity / behavioral / intent


class ShieldResult(NexusModel):
    """/v1/security/shield"""
    sanitized: bool | None = None
    blocked: bool | None = None
    payload: dict | None = None


class PqcSignResult(NexusModel):
    """/v1/security/pqc-sign"""
    signature: str | None = None
    algorithm: str | None = None   # "ML-DSA (Dilithium)"
    public_key: str | None = None


class ComplianceResult(NexusModel):
    """/v1/compliance/check and /v1/compliance/eu-ai-act"""
    compliant: bool | None = None
    frameworks: list[str] = Field(default_factory=list)
    certificate_id: str | None = None
    gaps: list[str] = Field(default_factory=list)


class AibomDriftResult(NexusModel):
    """/v1/aibom/drift"""
    drift_detected: bool | None = None
    lineage_hash: str | None = None
    verification_status: str | None = None


class AuditLogEntry(NexusModel):
    """/v1/audit/log"""
    entry_id: str | None = None
    hash: str | None = None
    timestamp: Any = None


class AuditVerifyResult(NexusModel):
    """/v1/audit/verify"""
    intact: bool | None = None
    chain_length: int | None = None
    first_entry: str | None = None
    last_entry: str | None = None


class QuarantineResult(NexusModel):
    """/v1/agent/quarantine"""
    quarantined: bool | None = None
    agent_id: str | None = None
    reason: str | None = None


# ── NEXUS AEGIS ───────────────────────────────────────────────────────────────

class AegisProxyResult(NexusModel):
    """/v1/aegis/mcp-proxy/execute"""
    allowed: bool | None = None
    tool_result: dict | None = None
    entropy_bound: float | None = None
    firewall_verdict: str | None = None


class EpistemicRouteResult(NexusModel):
    """/v1/aegis/router/epistemic-bound"""
    routed_to: str | None = None
    epsilon_bound: float | None = None
    rationale: str | None = None


class ComplianceCert(NexusModel):
    """/v1/aegis/certify-epoch (AEG-102 — 47-epoch drift + EU AI Act cert)"""
    certificate_id: str | None = None
    epoch: int | None = None
    eu_ai_act_compliant: bool | None = None
    drift_within_bound: bool | None = None


# ── Control Plane ─────────────────────────────────────────────────────────────

class AuthorizeActionResult(NexusModel):
    """/v1/authorize/action — OAP-100"""
    decision: str | None = None   # "allow" | "deny"
    risk_tier: str | None = None
    delegation_depth_ok: bool | None = None
    identity_check_passed: bool | None = None


class SpendingAuthResult(NexusModel):
    """/v1/spending/authorize — SPG-100"""
    approved: bool | None = None
    approved_amount_usdc: float | None = None
    tau_trust_decay: float | None = None


class SpendingBudgetResult(NexusModel):
    """/v1/spending/budget — SPG-101"""
    within_budget: bool | None = None
    total_spend_usdc: float | None = None
    per_hop: list[dict] = Field(default_factory=list)


class LineageRecord(NexusModel):
    """/v1/lineage/record — DLV-100"""
    record_id: str | None = None
    hash: str | None = None
    parent_hash: str | None = None
    hallucination_flagged: bool | None = None


class LineageTrace(NexusModel):
    """/v1/lineage/trace/{id} — DLV-101"""
    record_id: str | None = None
    hash_verified: bool | None = None
    chain: list[dict] = Field(default_factory=list)


class BehavioralContractResult(NexusModel):
    """/v1/contract/verify — BCV-100"""
    verified: bool | None = None
    contract_id: str | None = None
    d_max_ok: bool | None = None
    policy_epsilon_ok: bool | None = None
    tau_trust_ok: bool | None = None


class ContractAttestation(NexusModel):
    """/v1/contract/attestation/{id} — BCV-101"""
    attestation_id: str | None = None
    certificate: str | None = None
    valid_until: str | None = None


class FederationToken(NexusModel):
    """/v1/federation/mint — AIF-100"""
    token: str | None = None          # nxf_… prefixed
    identity_record: dict | None = None
    platforms: list[str] = Field(default_factory=list)


class FederationVerify(NexusModel):
    """/v1/federation/verify — AIF-101"""
    valid: bool | None = None
    identity_record: dict | None = None


class PortabilityCheck(NexusModel):
    """/v1/federation/portability — AIF-102"""
    portability_score: float | None = None
    from_platform: str | None = None
    to_platform: str | None = None
    capability_gaps: list[str] = Field(default_factory=list)


# ── Ecosystem Coordination ────────────────────────────────────────────────────

class ConsensusSession(NexusModel):
    """/v1/consensus/session — CSN-100"""
    session_id: str | None = None
    quorum_mode: str | None = None
    required_votes: int | None = None
    status: str | None = None


class ConsensusResult(NexusModel):
    """/v1/consensus/session/{id}/result — CSN-100"""
    session_id: str | None = None
    winning_hash: str | None = None
    certificate: str | None = None
    dissent_count: int | None = None
    quorum_met: bool | None = None


class QuotaTree(NexusModel):
    """/v1/quota/tree — QTA-100"""
    tree_id: str | None = None
    total_budget: int | None = None
    children: list[dict] = Field(default_factory=list)


class QuotaDrawResult(NexusModel):
    """/v1/quota/tree/{id}/draw — QTA-100"""
    drawn: int | None = None
    remaining: int | None = None
    idempotency_key: str | None = None


class QuotaStatus(NexusModel):
    """/v1/quota/tree/{id}/status — QTA-100"""
    tree_id: str | None = None
    remaining_budget: int | None = None
    per_child: dict | None = None
    soft_cap_alerts: list[str] = Field(default_factory=list)


class CertifiedOutput(NexusModel):
    """/v1/certify/output — OCN-100"""
    certificate_id: str | None = None
    score: float | None = None
    rubric_passed: bool | None = None
    valid_until: str | None = None


class SagaRollback(NexusModel):
    """/v1/rollback/saga — RBK-100"""
    saga_id: str | None = None
    steps: list[str] = Field(default_factory=list)
    status: str | None = None


class SagaCheckpoint(NexusModel):
    """/v1/rollback/saga/{id}/checkpoint — RBK-100"""
    saga_id: str | None = None
    step: str | None = None
    checkpointed: bool | None = None


class CompensationResult(NexusModel):
    """/v1/rollback/saga/{id}/compensate — RBK-100"""
    saga_id: str | None = None
    compensated_steps: list[str] = Field(default_factory=list)
    success: bool | None = None


class MemoryFence(NexusModel):
    """/v1/memory/fence — MFN-100"""
    fence_id: str | None = None
    namespace: str | None = None
    hmac_key_set: bool | None = None


class MemoryFenceAudit(NexusModel):
    """/v1/memory/fence/{id}/audit — MFN-100"""
    fence_id: str | None = None
    access_log: list[dict] = Field(default_factory=list)
    entry_count: int | None = None


# ── Trust Oracle ──────────────────────────────────────────────────────────────

class TrustScore(NexusModel):
    """/v1/trust/score — TCM-100"""
    agent_id: str | None = None
    score: float | None = None
    tier: str | None = None   # platinum / gold / silver / bronze / untrusted
    certified_monotonic: bool | None = None


class TrustHistory(NexusModel):
    """/v1/trust/history — TCM-101"""
    agent_id: str | None = None
    epochs: list[dict] = Field(default_factory=list)
    current_score: float | None = None


# ── DeFi Suite ────────────────────────────────────────────────────────────────

class DefiOptimize(NexusModel):
    """/v1/defi/optimize — DFP-100"""
    tick_range: dict | None = None
    fee_tier: str | None = None
    rebalance_schedule: str | None = None
    theorem: str | None = None   # "DFP-100-OptimalTick"


class DefiRiskScore(NexusModel):
    """/v1/defi/risk-score — DFI-101"""
    risk_score: float | None = None
    max_drawdown_bound: float | None = None   # certified 12.5%
    liquidation_probability_24h: float | None = None
    leverage: float | None = None


class DefiOracleVerify(NexusModel):
    """/v1/defi/oracle-verify — OGD-100"""
    manipulation_detected: bool | None = None
    flash_loan_score: float | None = None
    twap_attack_score: float | None = None


class LiquidationCheck(NexusModel):
    """/v1/defi/liquidation-check — LQS-100"""
    health_factor: float | None = None
    time_to_liquidation_s: int | None = None
    recommended_top_up_usdc: float | None = None


class BridgeVerify(NexusModel):
    """/v1/defi/bridge-verify — BRP-100"""
    safe: bool | None = None
    relay_reliability: float | None = None
    audit_score: float | None = None
    liquidity_depth_usdc: float | None = None


class SmartContractAudit(NexusModel):
    """/v1/defi/contract-audit — CVR-100"""
    certificate_id: str | None = None
    vulnerabilities_found: int | None = None
    patterns_checked: int | None = None
    risk_level: str | None = None


class YieldOptimize(NexusModel):
    """/v1/defi/yield-optimize — YLD-100"""
    allocations: list[dict] = Field(default_factory=list)
    expected_apy: float | None = None
    alpha_above_baseline: float | None = None


# ── Compliance Products ───────────────────────────────────────────────────────

class FairnessProof(NexusModel):
    """/v1/compliance/fairness — FNS-100"""
    disparate_impact_ratio: float | None = None
    within_bound: bool | None = None
    theorem: str | None = None   # "FNS-100-FairnessBound"


class ExplainCert(NexusModel):
    """/v1/compliance/explain — XPL-100"""
    certificate_id: str | None = None
    feature_attribution: dict | None = None
    gdpr_art22_ready: bool | None = None


class LineageProof(NexusModel):
    """/v1/compliance/lineage — LIN-100"""
    chain_hash: str | None = None
    stages: int | None = None
    integrity_ok: bool | None = None


class OversightEvent(NexusModel):
    """/v1/compliance/oversight — OVS-100"""
    event_id: str | None = None
    attestation: str | None = None
    reviewer: str | None = None
    timestamp: str | None = None


class IncidentReport(NexusModel):
    """/v1/compliance/incident — INC-100"""
    incident_id: str | None = None
    severity: str | None = None
    notification_deadline: str | None = None


class TransparencyReport(NexusModel):
    """/v1/compliance/transparency — TRP-100"""
    report_id: str | None = None
    period: str | None = None
    pdf_url: str | None = None
    machine_readable: dict | None = None


class DriftCheck(NexusModel):
    """/v1/drift/check — DRG-100"""
    drift_detected: bool | None = None
    psi_score: float | None = None
    bound: float | None = None   # ≤ 0.20 at 95% confidence
    theorem: str | None = None


class DriftCertificate(NexusModel):
    """/v1/drift/certificate — DRG-101"""
    certificate_id: str | None = None
    pdf_url: str | None = None
    linked_check_id: str | None = None


# ── Text AI ───────────────────────────────────────────────────────────────────

class TextSummary(NexusModel):
    """/v1/text/summarize"""
    summary: str | None = None
    compression_ratio: float | None = None
    sentences: int | None = None


class TextKeywords(NexusModel):
    """/v1/text/keywords"""
    keywords: list[dict] = Field(default_factory=list)   # [{word, score}]
    top_keyword: str | None = None


class TextSentiment(NexusModel):
    """/v1/text/sentiment"""
    sentiment: str | None = None   # "positive" | "negative" | "neutral"
    confidence: float | None = None
    score: float | None = None


# ── Data Tools ────────────────────────────────────────────────────────────────

class DataValidation(NexusModel):
    """/v1/data/validate-json"""
    valid: bool | None = None
    errors: list[dict] = Field(default_factory=list)
    error_paths: list[str] = Field(default_factory=list)


class FormatConversion(NexusModel):
    """/v1/data/format-convert"""
    result: str | None = None
    from_format: str | None = None
    to_format: str | None = None


# ── Governance ────────────────────────────────────────────────────────────────

class GovernanceVote(NexusModel):
    """/v1/governance/vote — GOV-112"""
    vote_id: str | None = None
    accepted: bool | None = None
    trust_modifier: float | None = None


# ── Advanced Platform / Billing ───────────────────────────────────────────────

class EfficiencyResult(NexusModel):
    """/v1/efficiency — PAY-506"""
    roi_signal: float | None = None
    interactions_analysed: int | None = None
    efficiency_score: float | None = None


class BillingOutcome(NexusModel):
    """/v1/billing/outcome — PAY-509"""
    billable: bool | None = None
    amount_usdc: float | None = None
    success_metric: str | None = None


class CostAttribution(NexusModel):
    """/v1/costs/attribute — DEV-603"""
    total_tokens: int | None = None
    by_agent: dict | None = None
    by_task: dict | None = None
    by_model: dict | None = None


class MemoryTrimResult(NexusModel):
    """/v1/memory/trim — INF-815"""
    tokens_before: int | None = None
    tokens_after: int | None = None
    pruned_entries: int | None = None


class ThinkRoute(NexusModel):
    """/v1/routing/think — POP-1207"""
    complexity: Any = None   # "low" | "medium" | "high"
    recommended_tier: str | None = None
    recommended_model: str | None = None


class RoutingRecommend(NexusModel):
    """/v1/routing/recommend"""
    task_complexity: str | None = None
    optimal_model: str | None = None
    compression_level: str | None = None


class PaymentFee(NexusModel):
    """/v1/payments/fee — x402 fee oracle"""
    amount: Any = None
    currency: str | None = None
    network: str | None = None
    pay_to: str | None = None


# ── Developer Tools ───────────────────────────────────────────────────────────

class CryptoToolkit(NexusModel):
    """/v1/dcm/crypto-toolkit — DCM-1018"""
    blake3_hash: str | None = None
    merkle_proof: str | None = None
    nonce: str | None = None


class StarterKit(NexusModel):
    """/v1/dev/starter — DEV-601"""
    project_name: str | None = None
    files: dict | None = None
    x402_wired: bool | None = None


# ── BitNet 1.58-bit Inference ─────────────────────────────────────────────────

class BitNetModel(NexusModel):
    """One entry in GET /v1/bitnet/models (BIT-102)"""
    id: str | None = None
    provider: str | None = None
    params_b: float | None = None
    context_length: int | None = None
    memory_gb: float | None = None
    status: str | None = None


class BitNetModelsResponse(NexusModel):
    """GET /v1/bitnet/models"""
    models: list[BitNetModel] = Field(default_factory=list)
    count: int | None = None


class BitNetInferenceResponse(NexusModel):
    """POST /v1/bitnet/inference (BIT-100)"""
    result: str | None = None
    tokens_used: int | None = None
    model: str | None = None
    latency_ms: float | None = None
    ternary_ops: int | None = None


class BitNetBenchmarkResponse(NexusModel):
    """POST /v1/bitnet/benchmark (BIT-103)"""
    model: str | None = None
    tokens_per_second: float | None = None
    memory_mb: float | None = None
    latency_ms: float | None = None
    benchmark_id: str | None = None


class BitNetQuantizeResponse(NexusModel):
    """POST /v1/bitnet/quantize (BIT-104)"""
    quantized_model_id: str | None = None
    original_size_mb: float | None = None
    quantized_size_mb: float | None = None
    compression_ratio: float | None = None
    status: str | None = None


class BitNetStatus(NexusModel):
    """GET /v1/bitnet/status (BIT-105)"""
    status: str | None = None
    models_loaded: int | None = None
    requests_processed: int | None = None
    avg_latency_ms: float | None = None


# ── VANGUARD ─────────────────────────────────────────────────────────────────

class VanguardRedTeamResult(NexusModel):
    """POST /v1/vanguard/continuous-redteam"""
    run_id: str | None = None
    agent_id: str | None = None
    vulnerabilities_found: int | None = None
    severity: str | None = None
    findings: list[dict] = Field(default_factory=list)
    next_run_at: int | None = None


class VanguardMevRouteResult(NexusModel):
    """POST /v1/vanguard/mev/route-intent"""
    route_id: str | None = None
    approved: bool | None = None
    priority_score: float | None = None
    estimated_mev_usd: float | None = None
    slippage_within_tolerance: bool | None = None


class VanguardSessionResult(NexusModel):
    """POST /v1/vanguard/wallet/govern-session"""
    session_id: str | None = None
    governed: bool | None = None
    ucan_token: str | None = None
    expires_at: int | None = None


class VanguardEscrowResult(NexusModel):
    """POST /v1/vanguard/escrow/lock-and-verify"""
    lock_id: str | None = None
    verified: bool | None = None
    escrow_id: str | None = None
    amount_usdc: float | None = None
    status: str | None = None


# ── MEV Shield ────────────────────────────────────────────────────────────────

class MevProtectResult(NexusModel):
    """POST /v1/mev/protect (MEV-100)"""
    bundle_id: str | None = None
    protected: bool | None = None
    strategy: str | None = None
    estimated_mev_saved_usd: float | None = None
    submission_time_ms: int | None = None


class MevStatusResult(NexusModel):
    """GET /v1/mev/status (MEV-101)"""
    bundle_id: str | None = None
    status: str | None = None   # "pending" | "submitted" | "confirmed" | "failed"
    included_in_block: int | None = None
    mev_saved_usd: float | None = None


# ── Forge Marketplace ─────────────────────────────────────────────────────────

class ForgeLeaderboardEntry(NexusModel):
    agent_id: str | None = None
    name: str | None = None
    score: float | None = None
    rank: int | None = None
    badges: list[str] = Field(default_factory=list)


class ForgeLeaderboardResponse(NexusModel):
    """GET /v1/forge/leaderboard"""
    entries: list[ForgeLeaderboardEntry] = Field(default_factory=list)
    epoch: int | None = None


class ForgeVerifyResult(NexusModel):
    """POST /v1/forge/verify"""
    verified: bool | None = None
    agent_id: str | None = None
    score: float | None = None
    badge_awarded: str | None = None


class ForgeQuarantineResponse(NexusModel):
    """POST /v1/forge/quarantine"""
    quarantined: Any = None
    model_id: str | None = None
    reason: str | None = None
    count: int | None = None


class ForgeDeltaSubmitResult(NexusModel):
    """POST /v1/forge/delta/submit"""
    submission_id: str | None = None
    accepted: bool | None = None
    delta_score: float | None = None
    reward_usdc: float | None = None


class ForgeBadgeResult(NexusModel):
    """GET /v1/forge/badge/{id}"""
    badge_id: str | None = None
    name: str | None = None
    description: str | None = None
    image_url: str | None = None
    issued_at: str | None = None
    valid: bool | None = None


# ── Developer Tools: Docs / Lint / Certify ────────────────────────────────────

class DocsResult(NexusModel):
    ok: bool = False
    path: str | None = None
    files_generated: list[str] = []
    synthesis_applied: bool = False
    lora_captured: bool = False
    credit_used: float | None = None
    message: str | None = None


class LintResult(NexusModel):
    ok: bool = False
    path: str | None = None
    findings_count: int = 0
    findings: list[dict[str, Any]] = []
    linters_run: list[str] = []
    synthesis_applied: bool = False
    lora_captured: bool = False
    credit_used: float | None = None
    message: str | None = None


class CertifyResult(NexusModel):
    ok: bool = False
    path: str | None = None
    valid: bool = False
    root_digest: str | None = None
    signature: str | None = None
    signed_by: str | None = None
    issued_at: str | None = None
    lora_captured: bool = False
    credit_used: float | None = None
    certificate: dict[str, Any] = {}
    message: str | None = None


# ── Design Engine ─────────────────────────────────────────────────────────────

class DesignBlueprint(NexusModel):
    ok: bool = False
    description: str | None = None
    blueprint: dict[str, Any] = {}
    blueprint_id: str | None = None
    target_tiers: list[str] = []
    component_count: int = 0
    lora_captured: bool = False
    credit_used: float | None = None
    message: str | None = None


# ── Enhancement Engine ────────────────────────────────────────────────────────

class EnhanceScanResult(NexusModel):
    ok: bool = False
    path: str | None = None
    total_findings: int = 0
    findings: list[dict[str, Any]] = []
    blueprints_generated: int = 0
    lora_captured: bool = False
    credit_used: float | None = None
    message: str | None = None


class EnhanceApplyResult(NexusModel):
    ok: bool = False
    path: str | None = None
    applied_count: int = 0
    blueprints: list[dict[str, Any]] = []
    rebuild_triggered: bool = False
    certified: bool = False
    lora_captured: bool = False
    credit_used: float | None = None
    message: str | None = None

# `from __future__ import annotations` defers all annotation evaluation.
# Pydantic v2 needs explicit model_rebuild() for models with nested model fields
# so that forward-reference strings are resolved against the module's globals.
MCPTool.model_rebuild()
MCPManifest.model_rebuild()
