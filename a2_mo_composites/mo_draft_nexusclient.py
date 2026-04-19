# Extracted from C:/!ass-ade/src/ass_ade/nexus/client.py:202
# Component id: mo.source.ass_ade.nexusclient
from __future__ import annotations

__version__ = "0.1.0"

class NexusClient:
    """Typed client for all AAAA-Nexus API families.

    All methods accept ``**extra`` kwargs that are forwarded as JSON body or
    query params so callers can pass new fields without waiting for a client
    update.
    """

    def __init__(
        self,
        *,
        base_url: str,
        timeout: float = 20.0,
        transport: httpx.BaseTransport | None = None,
        api_key: str | None = None,
        agent_id: str | None = None,
    ) -> None:
        headers: dict[str, str] = {"User-Agent": "ass-ade/1.0.0"}
        if api_key:
            # Sanitize before injecting into HTTP headers (OWASP A03 — header injection).
            safe_key = sanitize_header_value(api_key.strip(), "api_key")
            headers["Authorization"] = f"Bearer {safe_key}"
            headers["X-API-Key"] = safe_key

        # X-Agent-Id lets the storefront deduct from the agent's accrued Nexus
        # credit balance on metered calls — so LoRA contributions automatically
        # discount future usage without requiring an API key or x402 payment.
        if agent_id:
            safe_agent_id = sanitize_header_value(agent_id.strip(), "agent_id")
            headers["X-Agent-Id"] = safe_agent_id

        self._client = httpx.Client(
            base_url=base_url.rstrip("/"),
            timeout=timeout,
            transport=transport,
            headers=headers,
        )

    def close(self) -> None:
        self._client.close()

    def __enter__(self) -> NexusClient:
        return self

    def __exit__(self, exc_type: object, exc: object, tb: object) -> None:
        self.close()

    # ── internal helpers ──────────────────────────────────────────────────────

    def _get_model(self, path: str, model_type: type[ModelT], **params: Any) -> ModelT:
        response = self._client.get(path, params=params or None)
        raise_for_status(response.status_code, endpoint=path)
        return model_type.model_validate(response.json())

    def _post_model(self, path: str, model_type: type[ModelT], body: dict | None = None) -> ModelT:
        response = self._client.post(path, json=body or {})
        raise_for_status(response.status_code, endpoint=path)
        return model_type.model_validate(response.json())

    def _post_raw(self, path: str, body: dict | None = None) -> Any:
        response = self._client.post(path, json=body or {})
        raise_for_status(response.status_code, endpoint=path)
        return response.json()

    def _get_raw(self, path: str, **params: Any) -> dict:
        response = self._client.get(path, params=params or None)
        raise_for_status(response.status_code, endpoint=path)
        return response.json()  # type: ignore[return-value]

    # ── Discovery & Protocol (free) ───────────────────────────────────────────

    def get_health(self) -> HealthStatus:
        """/health — free"""
        return self._get_model("/health", HealthStatus)

    def get_openapi(self) -> OpenApiDocument:
        """/openapi.json — free"""
        return self._get_model("/openapi.json", OpenApiDocument)

    def get_agent_card(self) -> AgentCard:
        """/.well-known/agent.json — A2A capability manifest, free"""
        return self._get_model("/.well-known/agent.json", AgentCard)

    def get_mcp_manifest(self) -> MCPManifest:
        """/.well-known/mcp.json — MCP tool list, free"""
        return self._get_model("/.well-known/mcp.json", MCPManifest)

    def get_pricing_manifest(self) -> PricingManifest:
        """/.well-known/pricing.json — machine-readable tiers, free"""
        return self._get_model("/.well-known/pricing.json", PricingManifest)

    def get_payment_fee(self) -> PaymentFee:
        """/v1/payments/fee — current x402 payment requirements, free"""
        return self._get_model("/v1/payments/fee", PaymentFee)

    def get_metrics(self) -> PlatformMetrics:
        """/v1/metrics — aggregated public telemetry, free"""
        return self._get_model("/v1/metrics", PlatformMetrics)

    # ── x402 Payment Handling ──────────────────────────────────────────────

    def handle_x402(self, response: httpx.Response) -> dict:
        """Parse a 402 Payment Required response and return payment details.

        The x402 protocol returns payment requirements in the response body.
        This method parses the response into a dict that includes both backward-compatible
        keys and a typed PaymentChallenge for new code.

        Returns a dict with:
        - payment_required: bool (always True)
        - challenge: PaymentChallenge (typed, parsed from response)
        - amount_usdc: float (from challenge.amount_usdc)
        - network: str (blockchain network)
        - treasury: str (payment recipient)
        - endpoint: str (which endpoint requires payment)
        - detail: str (human-readable message)
        - raw: dict (original response body)
        """
        try:
            body = response.json()
        except ValueError:
            body = {}

        # Try to parse as a typed PaymentChallenge
        challenge = None
        try:
            challenge = PaymentChallenge.from_response(body)
        except ValueError:
            pass  # Fall back to loose dict format

        return {
            "payment_required": True,
            "challenge": challenge,  # New: typed PaymentChallenge
            "amount_usdc": body.get("amount") or body.get("price_usdc", 0),
            "network": body.get("network", "base"),
            "treasury": body.get("address") or body.get("treasury", ""),
            "endpoint": body.get("endpoint", ""),
            "detail": body.get("detail") or body.get("message", "Payment required"),
            "raw": body,
        }

    def _post_with_x402(self, path: str, body: dict | None = None) -> dict:
        """POST that gracefully handles 402 by returning payment details instead of raising."""
        response = self._client.post(path, json=body or {})
        if response.status_code == 402:
            return self.handle_x402(response)
        raise_for_status(response.status_code, endpoint=path)
        return response.json()  # type: ignore[return-value]

    def post_with_x402(self, path: str, body: dict | None = None) -> dict:
        """POST handling x402 Payment Required gracefully.

        Returns a dict with payment details instead of raising when a 402 is received.
        Includes both backward-compatible keys and a typed 'challenge' PaymentChallenge object.
        """
        return self._post_with_x402(path, body)

    def request_with_payment_headers(
        self,
        path: str,
        body: dict | None = None,
        *,
        payment_headers: dict[str, str],
    ) -> httpx.Response:
        """POST to *path* with *payment_headers* merged in.

        Use this for the second leg of an x402 payment flow, where the
        payment proof headers (from the wallet) must accompany the actual request.
        """
        # Sanitize all header values before forwarding to prevent header injection
        # when this method is called with user-controlled payment proof headers (OWASP A03).
        safe_headers = {
            k: sanitize_header_value(str(v), f"payment_headers[{k!r}]")
            for k, v in payment_headers.items()
        }
        return self._client.post(path, json=body or {}, headers=safe_headers)

    # ── Internal Search (owner-only RAG) ─────────────────────────────────

    def internal_search(self, query: str, max_results: int = 10, session_token: str | None = None) -> list[dict]:
        """POST /internal/search — semantic search over the private knowledge base.

        Requires owner session token.
        """
        headers = {}
        if session_token:
            # Sanitize before inserting into an HTTP header (OWASP A03).
            headers["X-Owner-Token"] = sanitize_header_value(session_token.strip(), "session_token")
        response = self._client.post(
            "/internal/search",
            json={"query": query, "max_results": max_results},
            headers=headers,
        )
        raise_for_status(response.status_code, endpoint="/internal/search")
        return response.json()  # type: ignore[return-value]

    def internal_search_chat(self, query: str, session_token: str | None = None, **kwargs: Any) -> dict:
        """POST /internal/search/chat — RAG search + LLM answer.

        Requires owner session token.
        """
        headers = {}
        if session_token:
            # Sanitize before inserting into an HTTP header (OWASP A03).
            headers["X-Owner-Token"] = sanitize_header_value(session_token.strip(), "session_token")
        response = self._client.post(
            "/internal/search/chat",
            json={"query": query, **kwargs},
            headers=headers,
        )
        raise_for_status(response.status_code, endpoint="/internal/search/chat")
        return response.json()  # type: ignore[return-value]

    # ── AI Inference ──────────────────────────────────────────────────────────

    def inference(self, prompt: str, **kwargs: Any) -> InferenceResponse:
        """/v1/inference — Llama 3.1 8B via Cloudflare Workers AI. $0.060/call"""
        return self._post_model("/v1/inference", InferenceResponse, {"prompt": prompt, **kwargs})

    def inference_stream(self, prompt: str, **kwargs: Any) -> Iterator[str]:
        """/v1/inference/stream — streaming CoT inference. $0.100/call

        Yields text chunks as they arrive via SSE / chunked response.
        """
        with self._client.stream("POST", "/v1/inference/stream", json={"prompt": prompt, **kwargs}) as r:
            r.raise_for_status()
            for chunk in r.iter_text():
                if chunk:
                    yield chunk

    def embed(self, values: list[float], **kwargs: Any) -> EmbedResponse:
        """/v1/embed — HELIX compressed embedding. $0.040/request"""
        return self._post_model("/v1/embed", EmbedResponse, {"values": values, **kwargs})

    # ── Hallucination / Trust Oracles ─────────────────────────────────────────

    def hallucination_oracle(self, text: str, **kwargs: Any) -> HallucinationResult:
        """/v1/oracle/hallucination — certified upper bound on confabulation. $0.040/request"""
        return self._post_model("/v1/oracle/hallucination", HallucinationResult, {"text": text, **kwargs})

    def trust_phase_oracle(self, agent_id: str, **kwargs: Any) -> TrustPhaseResult:
        """/v1/oracle/v-ai — V_AI geometric trust phase. $0.020/request"""
        return self._post_model("/v1/oracle/v-ai", TrustPhaseResult, {"agent_id": agent_id, **kwargs})

    def entropy_oracle(self, **kwargs: Any) -> EntropyResult:
        """/v1/oracle/entropy — session entropy measurement. $0.004/call"""
        return self._post_model("/v1/oracle/entropy", EntropyResult, kwargs or {})

    def trust_decay(self, agent_id: str, epochs: int, **kwargs: Any) -> TrustDecayResult:
        """/v1/trust/decay — P2P trust decay oracle. $0.008/call"""
        return self._post_model("/v1/trust/decay", TrustDecayResult, {"agent_id": agent_id, "epochs": epochs, **kwargs})

    # ── RatchetGate — session security (CVE-2025-6514 fix) ───────────────────

    def ratchet_register(self, agent_id: int, **kwargs: Any) -> RatchetSession:
        """/v1/ratchet/register — new session with epoch counter. agent_id must be a multiple of G_18 (324). $0.008/call"""
        return self._post_model("/v1/ratchet/register", RatchetSession, {"agent_id": agent_id, **kwargs})

    def ratchet_advance(self, session_id: str, **kwargs: Any) -> RatchetAdvance:
        """/v1/ratchet/advance — advance epoch + re-key. $0.008/call"""
        return self._post_model("/v1/ratchet/advance", RatchetAdvance, {"session_id": session_id, **kwargs})

    def ratchet_probe(self, session_ids: list[str], **kwargs: Any) -> RatchetProbeResult:
        """/v1/ratchet/probe — batch liveness check for up to 100 sessions. $0.008/call"""
        return self._post_model("/v1/ratchet/probe", RatchetProbeResult, {"session_ids": session_ids, **kwargs})

    def ratchet_status(self, session_id: str) -> RatchetStatus:
        """/v1/ratchet/status/{id} — epoch + remaining calls. $0.004/call"""
        return self._get_model(f"/v1/ratchet/status/{_pseg(session_id, 'session_id')}", RatchetStatus)

    # ── VeriRand ──────────────────────────────────────────────────────────────

    def rng_quantum(self, count: int = 1, **kwargs: Any) -> RngResult:
        """/v1/rng/quantum — quantum-seeded RNG with proof. $0.020/request"""
        return self._get_model("/v1/rng/quantum", RngResult, count=count, **kwargs)

    def rng_verify(self, seed_ts: str, numbers: str, proof: str) -> dict:
        """/v1/rng/verify — verify HMAC proof offline. Free"""
        return self._get_model(  # type: ignore[return-value]
            "/v1/rng/verify", RngResult, seed_ts=seed_ts, numbers=numbers, proof=proof
        ).model_dump()

    # ── VRF Gaming ────────────────────────────────────────────────────────────

    def vrf_draw(self, range_min: int, range_max: int, count: int = 1, **kwargs: Any) -> VrfDraw:
        """/v1/vrf/draw — VRF random draw with on-chain proof. $0.01 + 0.5% of pot"""
        return self._post_model("/v1/vrf/draw", VrfDraw, {"range_min": range_min, "range_max": range_max, "count": count, **kwargs})

    def vrf_verify_draw(self, draw_id: str, **kwargs: Any) -> VrfVerify:
        """/v1/vrf/verify-draw — verify a prior draw. Included with draw"""
        return self._post_model("/v1/vrf/verify-draw", VrfVerify, {"draw_id": draw_id, **kwargs})

    # ── VeriDelegate — UCAN delegation chains ────────────────────────────────

    def delegate_verify(
        self,
        chain: list[dict] | None = None,
        *,
        token: str | None = None,
        **kwargs: Any,
    ) -> DelegationValidation:
        """/v1/delegate/verify — full UCAN chain validation (D_MAX=23). $0.080/call"""
        if chain is None:
            chain = [{"token": token}] if token is not None else []
        return self._post_model("/v1/delegate/verify", DelegationValidation, {"chain": chain, **kwargs})

    def delegate_receipt(self, receipt_id: str) -> DelegateReceipt:
        """/v1/delegate/receipt/{id} — signed delegation receipt. $0.020/call"""
        return self._get_model(f"/v1/delegate/receipt/{_pseg(receipt_id, 'receipt_id')}", DelegateReceipt)

    def delegation_validate(self, chain: list[dict], **kwargs: Any) -> DelegationValidation:
        """/v1/identity/delegation/validate — IDT-201 chain depth validator. $0.080/call"""
        return self._post_model("/v1/identity/delegation/validate", DelegationValidation, {"chain": chain, **kwargs})

    # ── Identity & Auth ───────────────────────────────────────────────────────

    def identity_verify(self, actor: str | None = None, *, agent_id: str | None = None, **kwargs: Any) -> IdentityVerification:
        """/v1/identity/verify — topology-grounded identity proof. $0.080/request"""
        return self._post_model("/v1/identity/verify", IdentityVerification, {"actor": actor or agent_id or "", **kwargs})

    def sybil_check(self, actor: str | None = None, *, agent_id: str | None = None, **kwargs: Any) -> SybilCheckResult:
        """/v1/identity/sybil-check — sybil resistance check. $0.020/call"""
        return self._post_model("/v1/identity/sybil-check", SybilCheckResult, {"actor": actor or agent_id or "", **kwargs})

    def zero_trust_auth(self, agent_id: int, endpoint: str, capability: str, trust: float = 0.9984, **kwargs: Any) -> ZeroTrustResult:
        """/v1/auth/zero-trust — zero-trust auth primitive. agent_id must be a multiple of G_18 (324). $0.020/call"""
        return self._post_model("/v1/auth/zero-trust", ZeroTrustResult, {
            "agent_id": agent_id, "endpoint": endpoint, "capability": capability, "trust": trust, **kwargs,
        })

    # ── Agent Escrow ──────────────────────────────────────────────────────────

    def escrow_create(self, amount_usdc: float, sender: str, receiver: str, conditions: list[str], **kwargs: Any) -> EscrowCreated:
        """/v1/escrow/create — lock USDC with release conditions. $0.040/call"""
        return self._post_model("/v1/escrow/create", EscrowCreated, {
            "amount_usdc": amount_usdc, "sender": sender, "receiver": receiver,
            "conditions": conditions, **kwargs,
        })

    def escrow_release(self, escrow_id: str, proof: str, **kwargs: Any) -> EscrowResult:
        """/v1/escrow/release — release funds with completion proof. $0.020/call"""
        return self._post_model("/v1/escrow/release", EscrowResult, {"escrow_id": escrow_id, "proof": proof, **kwargs})

    def escrow_status(self, escrow_id: str) -> EscrowStatus:
        """/v1/escrow/status/{id} — check escrow state. $0.008/call"""
        return self._get_model(f"/v1/escrow/status/{_pseg(escrow_id, 'escrow_id')}", EscrowStatus)

    def escrow_dispute(
        self,
        escrow_id: str,
        evidence: str | None = None,
        *,
        reason: str | None = None,
        **kwargs: Any,
    ) -> EscrowResult:
        """/v1/escrow/dispute — open dispute with evidence. $0.060/call"""
        dispute_evidence = evidence or reason or ""
        return self._post_model("/v1/escrow/dispute", EscrowResult, {"escrow_id": escrow_id, "evidence": dispute_evidence, **kwargs})

    def escrow_arbitrate(self, escrow_id: str, vote: str, **kwargs: Any) -> EscrowResult:
        """/v1/escrow/arbitrate — cast arbiter vote (3-vote majority). $0.020/call"""
        return self._post_model("/v1/escrow/arbitrate", EscrowResult, {"escrow_id": escrow_id, "vote": vote, **kwargs})

    # ── Reputation Ledger ─────────────────────────────────────────────────────

    def reputation_score(self, agent_id: str) -> ReputationScore:
        """/v1/reputation/score/{id} — tier + fee multiplier. $0.008/call"""
        return self._get_model(f"/v1/reputation/score/{_pseg(agent_id, 'agent_id')}", ReputationScore)

    def reputation_history(self, agent_id: str) -> ReputationHistory:
        """/v1/reputation/history/{id} — exponential-decay weighted history. $0.012/call"""
        return self._get_model(f"/v1/reputation/history/{_pseg(agent_id, 'agent_id')}", ReputationHistory)

    def reputation_record(self, agent_id: str, success: bool = True, quality: float = 1.0, latency_ms: float = 0.0, **kwargs: Any) -> ReputationRecord:
        """/v1/reputation/record — append a reputation event. $0.008/call"""
        return self._post_model("/v1/reputation/record", ReputationRecord, {
            "agent_id": agent_id, "success": success, "quality": quality, "latency_ms": latency_ms, **kwargs,
        })

    def reputation_dispute(self, entry_id: str, reason: str, **kwargs: Any) -> dict:
        """/v1/reputation/dispute — challenge an entry. $0.080/call"""
        return self._post_raw("/v1/reputation/dispute", {"entry_id": entry_id, "reason": reason, **kwargs})

    # ── SLA Engine ────────────────────────────────────────────────────────────

    def sla_register(self, agent_id: str, latency_ms: float, uptime_pct: float, error_rate: float, bond_usdc: float, **kwargs: Any) -> SlaRegistration:
        """/v1/sla/register — commit to SLA with bond. $0.080/call"""
        return self._post_model("/v1/sla/register", SlaRegistration, {
            "agent_id": agent_id, "latency_ms": latency_ms, "uptime_pct": uptime_pct,
            "error_rate": error_rate, "bond_usdc": bond_usdc, **kwargs,
        })

    def sla_report(self, sla_id: str, metric: str, value: float, **kwargs: Any) -> SlaResult:
        """/v1/sla/report — report SLA metric, auto-detects breaches. $0.020/call"""
        return self._post_model("/v1/sla/report", SlaResult, {"sla_id": sla_id, "metric": metric, "value": value, **kwargs})

    def sla_status(self, sla_id: str) -> SlaStatus:
        """/v1/sla/status/{id} — compliance score + bond remaining. $0.008/call"""
        return self._get_model(f"/v1/sla/status/{_pseg(sla_id, 'sla_id')}", SlaStatus)

    def sla_breach(self, sla_id: str, severity: str, **kwargs: Any) -> SlaResult:
        """/v1/sla/breach — report breach + calculate penalty. $0.040/call"""
        return self._post_model("/v1/sla/breach", SlaResult, {"sla_id": sla_id, "severity": severity, **kwargs})

    # ── Agent Discovery ───────────────────────────────────────────────────────

    def discovery_search(self, capability: str, **kwargs: Any) -> DiscoveryResult:
        """/v1/discovery/search — search by capability, reputation-ranked. $0.060/call"""
        return self._post_model("/v1/discovery/search", DiscoveryResult, {"capability": capability, **kwargs})

    def discovery_recommend(self, task: str, **kwargs: Any) -> DiscoveryResult:
        """/v1/discovery/recommend — AI-ranked recommendations from task description. $0.040/call"""
        return self._post_model("/v1/discovery/recommend", DiscoveryResult, {"task": task, **kwargs})

    def discovery_registry(self, **kwargs: Any) -> AgentRegistry:
        """/v1/discovery/registry — browse all registered agents. $0.020/call"""
        return self._get_model("/v1/discovery/registry", AgentRegistry, **kwargs)

    # ── Agent Swarm & Routing ─────────────────────────────────────────────────

    def agent_register(self, agent_id: int, name: str, capabilities: list[str], endpoint: str, **kwargs: Any) -> AgentRegistration:
        """POST /v1/agents/register — agent_id must be a multiple of G_18 (324). Free"""
        return self._post_model("/v1/agents/register", AgentRegistration, {
            "agent_id": agent_id, "name": name, "capabilities": capabilities, "endpoint": endpoint, **kwargs,
        })

    def agent_topology(self, **kwargs: Any) -> AgentTopology:
        """/v1/agents/topology — global swarm topology. $0.008/call"""
        return self._get_model("/v1/agents/topology", AgentTopology, **kwargs)

    def agent_semantic_diff(self, base: str, current: str, **kwargs: Any) -> SemanticDiff:
        """/v1/agents/semantic-diff — knowledge drift detection (Jaccard). $0.040/request"""
        return self._post_model("/v1/agents/semantic-diff", SemanticDiff, {"base": base, "current": current, **kwargs})

    def agent_intent_classify(self, text: str, **kwargs: Any) -> IntentClassification:
        """/v1/agents/intent-classify — top-3 intents with confidence. $0.020/request"""
        return self._post_model("/v1/agents/intent-classify", IntentClassification, {"text": text, **kwargs})

    def agent_reputation(self, agent_id: str, **kwargs: Any) -> dict:
        """/v1/agents/reputation — A2A compliance + trust score. $0.040/request"""
        return self._post_raw("/v1/agents/reputation", {"agent_id": agent_id, **kwargs})

    def agent_token_budget(self, task: str, models: list[str] | None = None, **kwargs: Any) -> TokenBudget:
        """/v1/agents/token-budget — cost estimate across 7 models. $0.020/request"""
        return self._post_model("/v1/agents/token-budget", TokenBudget, {"task": task, "models": models or [], **kwargs})

    def agent_contradiction(self, statement_a: str, statement_b: str, **kwargs: Any) -> ContradictionResult:
        """/v1/agents/contradiction — NLI fact-checker for two statements. $0.020/request"""
        return self._post_model("/v1/agents/contradiction", ContradictionResult, {
            "statement_a": statement_a, "statement_b": statement_b, **kwargs,
        })

    def agent_plan(self, goal: str, **kwargs: Any) -> AgentPlan:
        """/v1/agents/plan — decompose goal into dependency-aware steps. $0.060/request"""
        return self._post_model("/v1/agents/plan", AgentPlan, {"goal": goal, **kwargs})

    def agent_capabilities_match(self, task: str, **kwargs: Any) -> CapabilityMatch:
        """/v1/agents/capabilities/match — find matching agents in the swarm. $0.020/request"""
        return self._post_model("/v1/agents/capabilities/match", CapabilityMatch, {"task": task, **kwargs})

    def swarm_relay(self, from_id: str, to: str, message: dict, ttl: int = 3600, **kwargs: Any) -> SwarmRelayResult:
        """/v1/swarm/relay — A2A-ENT message relay across swarm. $0.008/call"""
        return self._post_model("/v1/swarm/relay", SwarmRelayResult, {"from": from_id, "to": to, "message": message, "ttl": ttl, **kwargs})

    def swarm_inbox(self, agent_id: str, **kwargs: Any) -> SwarmRelayResult:
        """/v1/swarm/inbox — agent message inbox. $0.008/call"""
        return self._get_model("/v1/swarm/inbox", SwarmRelayResult, agent_id=agent_id, **kwargs)

    # ── Prompt Intelligence & Ethics ──────────────────────────────────────────

    def prompt_inject_scan(self, prompt: str, **kwargs: Any) -> PromptScanResult:
        """/v1/prompts/inject-scan — adversarial injection detection. $0.040/request"""
        return self._post_model("/v1/prompts/inject-scan", PromptScanResult, {"prompt": prompt, **kwargs})

    def prompt_optimize(self, prompt: str, **kwargs: Any) -> PromptOptimized:
        """/v1/prompts/optimize — rewrite for clarity, safety, lower cost. $0.040/request"""
        return self._post_model("/v1/prompts/optimize", PromptOptimized, {"prompt": prompt, **kwargs})

    def prompt_download(self) -> dict:
        """/v1/prompts/download — curated agent-ready prompt library. Free"""
        return self._get_raw("/v1/prompts/download")

    def security_prompt_scan(self, prompt: str, **kwargs: Any) -> PromptScanResult:
        """/v1/security/prompt-scan — detect + block adversarial inputs. $0.040/request"""
        return self._post_model("/v1/security/prompt-scan", PromptScanResult, {"prompt": prompt, **kwargs})

    def ethics_check(self, text: str, **kwargs: Any) -> EthicsCheckResult:
        """/v1/ethics/check — Prime Axiom ethical oracle (DCM-1017). $0.040/request"""
        return self._post_model("/v1/ethics/check", EthicsCheckResult, {"text": text, **kwargs})

    def security_zero_day(self, payload: dict, **kwargs: Any) -> ZeroDayResult:
        """/v1/security/zero-day — zero-day pattern detector for agent payloads. $0.040/request"""
        return self._post_model("/v1/security/zero-day", ZeroDayResult, {"payload": payload, **kwargs})

    # ── Security & Compliance ─────────────────────────────────────────────────

    def threat_score(self, payload: dict, **kwargs: Any) -> ThreatScore:
        """/v1/threat/score — multi-vector threat scoring (SEC-303). $0.040/request"""
        return self._post_model("/v1/threat/score", ThreatScore, {"payload": payload, **kwargs})

    def security_shield(self, payload: dict, **kwargs: Any) -> ShieldResult:
        """/v1/security/shield — payload sanitization layer for agentic tool calls. $0.040/request"""
        return self._post_model("/v1/security/shield", ShieldResult, {"payload": payload, **kwargs})

    def security_pqc_sign(self, data: str, **kwargs: Any) -> PqcSignResult:
        """/v1/security/pqc-sign — ML-DSA (Dilithium) post-quantum signatures. $0.020/request"""
        return self._post_model("/v1/security/pqc-sign", PqcSignResult, {"data": data, **kwargs})

    def compliance_check(self, system_description: str, **kwargs: Any) -> ComplianceResult:
        """/v1/compliance/check — EU AI Act / NIST AI RMF / ISO 42001 (CMP-100). $0.040/check"""
        return self._post_model("/v1/compliance/check", ComplianceResult, {"system_description": system_description, **kwargs})

    def compliance_eu_ai_act(self, system_description: str, **kwargs: Any) -> ComplianceResult:
        """/v1/compliance/eu-ai-act — Annex IV conformity certificate. $0.040/check"""
        return self._post_model("/v1/compliance/eu-ai-act", ComplianceResult, {"system_description": system_description, **kwargs})

    def aibom_drift(self, model_id: str, **kwargs: Any) -> AibomDriftResult:
        """/v1/aibom/drift — AIBOM lineage verification (AIB-401). $0.040/request"""
        return self._post_model("/v1/aibom/drift", AibomDriftResult, {"model_id": model_id, **kwargs})

    def audit_log(self, event: dict, **kwargs: Any) -> AuditLogEntry:
        """/v1/audit/log — tamper-evident event logging (GOV-103). $0.040/request"""
        return self._post_model("/v1/audit/log", AuditLogEntry, {"event": event, **kwargs})

    def audit_verify(self, **kwargs: Any) -> AuditVerifyResult:
        """/v1/audit/verify — verify audit trail integrity. $0.040/request"""
        return self._post_model("/v1/audit/verify", AuditVerifyResult, kwargs or {})

    def agent_quarantine(self, agent_id: str, reason: str, **kwargs: Any) -> QuarantineResult:
        """/v1/agent/quarantine — isolate non-compliant agents (SEC-309). $0.040/request"""
        return self._post_model("/v1/agent/quarantine", QuarantineResult, {"agent_id": agent_id, "reason": reason, **kwargs})

    # ── NEXUS AEGIS ───────────────────────────────────────────────────────────

    def aegis_mcp_proxy(
        self,
        tool: str | None = None,
        tool_input: str = "",
        agent_id: str | None = None,
        *,
        tool_name: str | None = None,
        payload: dict[str, Any] | None = None,
        **kwargs: Any,
    ) -> AegisProxyResult:
        """/v1/aegis/mcp-proxy/execute — MCP tool-call firewall (AEG-100). $0.040/call"""
        resolved_tool = tool or tool_name or ""
        resolved_tool_input = tool_input
        if payload is not None and not resolved_tool_input:
            resolved_tool_input = json.dumps(payload)
        body: dict[str, Any] = {"tool": resolved_tool, "tool_input": resolved_tool_input, **kwargs}
        if agent_id:
            body["agent_id"] = agent_id
        return self._post_model("/v1/aegis/mcp-proxy/execute", AegisProxyResult, body)

    def aegis_epistemic_route(
        self,
        prompt: str | None = None,
        max_tokens: int = 256,
        model: str = "auto",
        *,
        query: str | None = None,
        **kwargs: Any,
    ) -> EpistemicRouteResult:
        """/v1/aegis/router/epistemic-bound — epistemic-aware routing (AEG-101). $0.040/call"""
        return self._post_model("/v1/aegis/router/epistemic-bound", EpistemicRouteResult, {
            "prompt": prompt or query or "", "max_tokens": max_tokens, "model": model, **kwargs,
        })

    def aegis_certify_epoch(self, system_id: str | None = None, *, agent_id: str | None = None, **kwargs: Any) -> ComplianceCert:
        """/v1/aegis/certify-epoch — 47-epoch drift + EU AI Act cert (AEG-102). $0.060/call"""
        return self._post_model("/v1/aegis/certify-epoch", ComplianceCert, {"system_id": system_id or agent_id or "", **kwargs})

    # ── Control Plane ─────────────────────────────────────────────────────────

    def authorize_action(self, agent_id: str, action: str, delegation_depth: int = 0, **kwargs: Any) -> AuthorizeActionResult:
        """/v1/authorize/action — pre-action authorization gateway (OAP-100). $0.040/call"""
        return self._post_model("/v1/authorize/action", AuthorizeActionResult, {
            "agent_id": agent_id, "action": action, "delegation_depth": delegation_depth, **kwargs,
        })

    def spending_authorize(self, agent_id: str, amount_usdc: float, epoch: int = 0, **kwargs: Any) -> SpendingAuthResult:
        """/v1/spending/authorize — trust-decay spending bound (SPG-100). $0.040/call"""
        return self._post_model("/v1/spending/authorize", SpendingAuthResult, {
            "agent_id": agent_id, "amount_usdc": amount_usdc, "epoch": epoch, **kwargs,
        })

    def spending_budget(
        self,
        chain: list[dict] | None = None,
        total_usdc: float = 0.0,
        *,
        agent_id: str | None = None,
        **kwargs: Any,
    ) -> SpendingBudgetResult:
        """/v1/spending/budget — multi-hop chain budget (SPG-101). $0.040/call"""
        resolved_chain = chain or ([{"agent_id": agent_id}] if agent_id else [])
        return self._post_model("/v1/spending/budget", SpendingBudgetResult, {"chain": resolved_chain, "total_usdc": total_usdc, **kwargs})

    def lineage_record(
        self,
        intent: str | None = None,
        constraints: list[str] | None = None,
        outcome: str | None = None,
        *,
        agent_id: str | None = None,
        action: str | None = None,
        **kwargs: Any,
    ) -> LineageRecord:
        """/v1/lineage/record — hash-chained audit record (DLV-100). $0.060/call"""
        resolved_intent = intent or action or (f"agent:{agent_id}" if agent_id else "record")
        resolved_constraints = constraints or ([f"agent_id:{agent_id}"] if agent_id else [])
        resolved_outcome = outcome or action or "recorded"
        return self._post_model("/v1/lineage/record", LineageRecord, {
            "intent": resolved_intent, "constraints": resolved_constraints, "outcome": resolved_outcome, **kwargs,
        })

    def lineage_trace(self, record_id: str | None = None, *, lineage_id: str | None = None) -> LineageTrace:
        """/v1/lineage/trace/{id} — retrieve + verify chain integrity (DLV-100). $0.020/call"""
        resolved_record_id = record_id or lineage_id or ""
        return self._get_model(f"/v1/lineage/trace/{_pseg(resolved_record_id, 'record_id')}", LineageTrace)

    def contract_verify(self, contract: dict, **kwargs: Any) -> BehavioralContractResult:
        """/v1/contract/verify — validate against Codex formal bounds (BCV-100). $0.060/call"""
        return self._post_model("/v1/contract/verify", BehavioralContractResult, {"contract": contract, **kwargs})

    def contract_attestation(self, contract_id: str) -> ContractAttestation:
        """/v1/contract/attestation/{id} — fetch Nexus-Certified attestation (BCV-101). $0.020/call"""
        return self._get_model(f"/v1/contract/attestation/{_pseg(contract_id, 'contract_id')}", ContractAttestation)

    def federation_mint(
        self,
        identity: dict | None = None,
        platforms: list[str] | None = None,
        *,
        agent_id: str | None = None,
        scope: str | None = None,
        **kwargs: Any,
    ) -> FederationToken:
        """/v1/federation/mint — cross-platform nxf_ identity token (AIF-100). $0.040/call"""
        resolved_identity = identity or ({"agent_id": agent_id} if agent_id else {})
        resolved_platforms = platforms or ([scope] if scope else [])
        return self._post_model("/v1/federation/mint", FederationToken, {"identity": resolved_identity, "platforms": resolved_platforms, **kwargs})

    def federation_verify(self, token: str, **kwargs: Any) -> FederationVerify:
        """/v1/federation/verify — verify nxf_ token (AIF-101). $0.020/call"""
        return self._post_model("/v1/federation/verify", FederationVerify, {"token": token, **kwargs})

    def federation_portability(self, from_platform: str, to_platform: str, **kwargs: Any) -> PortabilityCheck:
        """/v1/federation/portability — cross-platform capability portability (AIF-102). $0.020/call"""
        return self._post_model("/v1/federation/portability", PortabilityCheck, {
            "from_platform": from_platform, "to_platform": to_platform, **kwargs,
        })

    # ── Ecosystem Coordination ──────────────────────────────────────────────────

    def consensus_vote(self, session_id: str, agent_id: str, output_hash: str, confidence: float, **kwargs: Any) -> dict:
        """/v1/consensus/session/{id}/vote — cast consensus vote. $0.020/call"""
        return self._post_raw(f"/v1/consensus/session/{_pseg(session_id, 'session_id')}/vote", {
            "agent_id": agent_id, "output_hash": output_hash, "confidence": confidence, **kwargs,
        })

    def consensus_result(self, session_id: str) -> ConsensusResult:
        """/v1/consensus/session/{id}/result — certified winning output. $0.020/call"""
        return self._get_model(f"/v1/consensus/session/{_pseg(session_id, 'session_id')}/result", ConsensusResult)

    def quota_tree_create(self, total_budget: int, children: list[str], **kwargs: Any) -> QuotaTree:
        """/v1/quota/tree — create budget tree (QME-100). $0.040/call"""
        return self._post_model("/v1/quota/tree", QuotaTree, {"total_budget": total_budget, "children": children, **kwargs})

    def quota_draw(self, tree_id: str, child_id: str, tokens: int, idempotency_key: str, **kwargs: Any) -> QuotaDrawResult:
        """/v1/quota/tree/{id}/draw — deduct tokens with idempotency. $0.020/call"""
        return self._post_model(f"/v1/quota/tree/{_pseg(tree_id, 'tree_id')}/draw", QuotaDrawResult, {
            "child_id": child_id, "tokens": tokens, "idempotency_key": idempotency_key, **kwargs,
        })

    def quota_status(self, tree_id: str) -> QuotaStatus:
        """/v1/quota/tree/{id}/status — remaining budget + alerts. $0.020/call"""
        return self._get_model(f"/v1/quota/tree/{_pseg(tree_id, 'tree_id')}/status", QuotaStatus)

    def certify_output(self, output: str, rubric: list[str], **kwargs: Any) -> CertifiedOutput:
        """/v1/certify/output — 30-day output certificate (OCN-100). $0.060/call"""
        return self._post_model("/v1/certify/output", CertifiedOutput, {"output": output, "rubric": rubric, **kwargs})

    def certify_output_verify(self, certificate_id: str) -> CertifiedOutput:
        """/v1/certify/output/{id}/verify — verify output certificate. $0.020/call"""
        return self._get_model(f"/v1/certify/output/{_pseg(certificate_id, 'certificate_id')}/verify", CertifiedOutput)

    def saga_register(self, name: str, steps: list[str], compensations: list[str], **kwargs: Any) -> SagaCheckpoint:
        """/v1/rollback/saga — create saga blueprint (RBK-100). $0.040/call"""
        return self._post_model("/v1/rollback/saga", SagaCheckpoint, {
            "name": name, "steps": steps, "compensations": compensations, **kwargs,
        })

    def saga_checkpoint(self, saga_id: str, step: str, **kwargs: Any) -> SagaCheckpoint:
        """/v1/rollback/saga/{id}/checkpoint — mark step completed (RBK-100). $0.020/call"""
        return self._post_model(f"/v1/rollback/saga/{_pseg(saga_id, 'saga_id')}/checkpoint", SagaCheckpoint, {"step": step, **kwargs})

    def saga_compensate(self, saga_id: str, **kwargs: Any) -> CompensationResult:
        """/v1/rollback/saga/{id}/compensate — LIFO rollback (RBK-100). $0.040/call"""
        return self._post_model(f"/v1/rollback/saga/{_pseg(saga_id, 'saga_id')}/compensate", CompensationResult, kwargs or {})

    def memory_fence_create(self, namespace: str, **kwargs: Any) -> MemoryFence:
        """/v1/memory/fence — cross-tenant HMAC namespace boundary (MFN-100). $0.040/call"""
        return self._post_model("/v1/memory/fence", MemoryFence, {"namespace": namespace, **kwargs})

    def memory_fence_audit(self, fence_id: str) -> MemoryFenceAudit:
        """/v1/memory/fence/{id}/audit — access log + entry count (MFN-100). $0.020/call"""
        return self._get_model(f"/v1/memory/fence/{_pseg(fence_id, 'fence_id')}/audit", MemoryFenceAudit)

    # ── Trust Oracle ──────────────────────────────────────────────────────────

    def trust_score(self, agent_id: str, **kwargs: Any) -> TrustScore:
        """/v1/trust/score — TCM-100 formally bounded score in [0,1]. $0.040/query"""
        return self._post_model("/v1/trust/score", TrustScore, {"agent_id": agent_id, **kwargs})

    def trust_history(self, agent_id: str, **kwargs: Any) -> TrustHistory:
        """/v1/trust/history — TCM-101 up to 100 epochs of score trajectory. $0.040/query"""
        return self._post_model("/v1/trust/history", TrustHistory, {"agent_id": agent_id, **kwargs})

    # ── v18 aliases — used by hook_map_terrain_gate / hook_trustbench_verify ──
    def trust_gate(self, agent_id: str, action: str = "default", **kwargs: Any) -> dict:
        """Trust gate decision: allowed iff trust_score >= TAU_TRUST.

        Falls back to trust_score lookup when /v1/trust/gate is unavailable.
        """
        try:
            return self._post_raw(
                "/v1/trust/gate",
                {"agent_id": agent_id, "action": action, **kwargs},
            )
        except Exception:
            try:
                score = self.trust_score(agent_id, **kwargs)
                score_val = float(getattr(score, "score", 0.0))
                return {
                    "allowed": score_val >= 0.998354361,
                    "score": score_val,
                    "fallback": "trust_score",
                }
            except Exception:
                return {"allowed": False, "score": 0.0, "fallback": "unavailable"}

    def map_terrain(self, required_capabilities: list, **kwargs: Any) -> dict:
        """Capability gap detection. Verdict PROCEED or HALT_AND_INVENT."""
        try:
            return self._post_raw(
                "/v1/map/terrain",
                {"required_capabilities": required_capabilities, **kwargs},
            )
        except Exception:
            return {
                "verdict": "PROCEED",
                "missing": [],
                "fallback": "local_assume_present",
            }

    def synthesize_verified_code(
        self, spec: str, language: str = "python", **kwargs: Any
    ) -> dict:
        """Formally-verified synthesis. Falls back to a stub with verified=False."""
        try:
            return self._post_raw(
                "/v1/synthesis/verified",
                {"spec": spec, "language": language, **kwargs},
            )
        except Exception:
            return {
                "code": f"# TODO unverified synthesis for: {spec[:120]}\npass\n",
                "verified": False,
                "fallback": "stub",
            }

    # ── DeFi Suite ────────────────────────────────────────────────────────────

    def defi_optimize(
        self,
        protocol: str | None = None,
        position_size_usdc: float | None = None,
        *,
        payload: dict | None = None,
        **kwargs: Any,
    ) -> DefiOptimize:
        """/v1/defi/optimize — optimal LP parameters (DFP-100). $0.08 + 0.2% of position"""
        if payload is not None:
            protocol = protocol or payload.get("protocol") or payload.get("pool") or payload.get("market")
            position_size_usdc = (
                position_size_usdc
                if position_size_usdc is not None
                else payload.get("position_size_usdc")
                or payload.get("amount_usdc")
                or payload.get("capital_usdc")
            )
        return self._post_model("/v1/defi/optimize", DefiOptimize, {
            "protocol": protocol or "", "position_size_usdc": position_size_usdc or 0.0, **kwargs,
        })

    def defi_risk_score(self, protocol: str, position: dict | None = None, **kwargs: Any) -> DefiRiskScore:
        """/v1/defi/risk-score — risk + max drawdown bound 12.5% (DFI-101). $0.08/call"""
        return self._post_model("/v1/defi/risk-score", DefiRiskScore, {"protocol": protocol, "position": position or {}, **kwargs})

    def defi_oracle_verify(
        self,
        pool: str | None = None,
        tvl_usdc: float = 0.0,
        *,
        oracle_id: str | None = None,
        **kwargs: Any,
    ) -> DefiOracleVerify:
        """/v1/defi/oracle-verify — flash loan + TWAP attack scoring (OGD-100). $0.04 + 0.1% TVL"""
        return self._post_model("/v1/defi/oracle-verify", DefiOracleVerify, {"pool": pool or oracle_id or "", "tvl_usdc": tvl_usdc, **kwargs})

    def defi_liquidation_check(self, position: dict | None = None, **kwargs: Any) -> LiquidationCheck:
        """/v1/defi/liquidation-check — health factor + time-to-liquidation (LQS-100). $0.04 + 1% equity"""
        resolved_position = position or {
            "position_id": kwargs.pop("position_id", None),
            "collateral_value": kwargs.pop("collateral_value", None),
            "debt_value": kwargs.pop("debt_value", None),
            "collateral_factor": kwargs.pop("collateral_factor", None),
        }
        return self._post_model("/v1/defi/liquidation-check", LiquidationCheck, {"position": resolved_position, **kwargs})

    def defi_bridge_verify(
        self,
        bridge: str | None = None,
        amount_usdc: float = 0.0,
        *,
        bridge_id: str | None = None,
        **kwargs: Any,
    ) -> BridgeVerify:
        """/v1/defi/bridge-verify — cross-chain bridge integrity (BRP-100). $0.08/verification"""
        return self._post_model("/v1/defi/bridge-verify", BridgeVerify, {"bridge": bridge or bridge_id or "", "amount_usdc": amount_usdc, **kwargs})

    def defi_contract_audit(self, contract_address: str, source_code: str | None = None, **kwargs: Any) -> SmartContractAudit:
        """/v1/defi/contract-audit — 30-pattern smart contract audit cert (CVR-100). $0.15/audit"""
        return self._post_model("/v1/defi/contract-audit", SmartContractAudit, {
            "contract_address": contract_address, "source_code": source_code, **kwargs,
        })

    def defi_yield_optimize(
        self,
        capital_usdc: float | None = None,
        protocols: list[str] | None = None,
        *,
        amount_usdc: float | None = None,
        risk_tolerance: str | None = None,
        **kwargs: Any,
    ) -> YieldOptimize:
        """/v1/defi/yield-optimize — optimal yield allocation (YLD-100). $0.04 + 2% alpha"""
        resolved_capital = capital_usdc if capital_usdc is not None else amount_usdc or 0.0
        resolved_protocols = protocols or []
        if risk_tolerance is not None:
            kwargs.setdefault("risk_tolerance", risk_tolerance)
        return self._post_model("/v1/defi/yield-optimize", YieldOptimize, {
            "capital_usdc": resolved_capital, "protocols": resolved_protocols, **kwargs,
        })

    # ── Compliance Products ───────────────────────────────────────────────────

    def compliance_fairness(self, dataset_description: str | None = None, *, model_id: str | None = None, **kwargs: Any) -> FairnessProof:
        """/v1/compliance/fairness — disparate impact ratio (FNS-100). $0.040/check"""
        return self._post_model("/v1/compliance/fairness", FairnessProof, {"dataset_description": dataset_description or model_id or "", **kwargs})

    def compliance_explain(self, output: str, input_features: dict, **kwargs: Any) -> ExplainCert:
        """/v1/compliance/explain — GDPR Art.22 explainability cert (XPL-100). $0.040/call"""
        return self._post_model("/v1/compliance/explain", ExplainCert, {"output": output, "input_features": input_features, **kwargs})

    def compliance_lineage(self, dataset_stages: list[dict], **kwargs: Any) -> LineageProof:
        """/v1/compliance/lineage — SHA-256 hash chain across dataset (LIN-100). $0.040/call"""
        return self._post_model("/v1/compliance/lineage", LineageProof, {"dataset_stages": dataset_stages, **kwargs})

    def compliance_oversight(self, reviewer: str, decision: str, **kwargs: Any) -> OversightEvent:
        """/v1/compliance/oversight — HITL review attestation (OVS-100). $0.020/event"""
        return self._post_model("/v1/compliance/oversight", OversightEvent, {"reviewer": reviewer, "decision": decision, **kwargs})

    def compliance_oversight_history(self, system_id: str, **kwargs: Any) -> dict:
        """/v1/compliance/oversight/history — paginated signed history (OVS-101). $0.020/query"""
        return self._get_raw("/v1/compliance/oversight/history", system_id=system_id, **kwargs)

    def compliance_incident(
        self,
        system_id: str | None = None,
        description: str | None = None,
        severity: str | None = None,
        *,
        incident_id: str | None = None,
        **kwargs: Any,
    ) -> IncidentReport:
        """/v1/compliance/incident — EU AI Act Art.73 incident report (INC-100). $0.020/report"""
        return self._post_model("/v1/compliance/incident", IncidentReport, {
            "system_id": system_id or incident_id or "",
            "description": description or "CLI incident report",
            "severity": severity or "medium",
            **kwargs,
        })

    def compliance_incidents(self, system_id: str, **kwargs: Any) -> dict:
        """/v1/compliance/incidents — incident registry query (INC-101). $0.020/query"""
        return self._get_raw("/v1/compliance/incidents", system_id=system_id, **kwargs)

    def compliance_transparency(self, system_id: str, period: str, **kwargs: Any) -> TransparencyReport:
        """/v1/compliance/transparency — quarterly transparency report (TRP-100). $0.080/report"""
        return self._post_model("/v1/compliance/transparency", TransparencyReport, {
            "system_id": system_id, "period": period, **kwargs,
        })

    def drift_check(
        self,
        model_id: str,
        reference_data: dict | None = None,
        current_data: dict | None = None,
        **kwargs: Any,
    ) -> DriftCheck:
        """/v1/drift/check — PSI drift detection ≤0.20 (DRG-100). $0.010/check"""
        return self._post_model("/v1/drift/check", DriftCheck, {
            "model_id": model_id,
            "reference_data": reference_data or {},
            "current_data": current_data or {},
            **kwargs,
        })

    def drift_certificate(self, check_id: str | None = None, *, model_id: str | None = None) -> DriftCertificate:
        """/v1/drift/certificate — signed drift compliance cert (DRG-101). $0.010/cert"""
        return self._get_model("/v1/drift/certificate", DriftCertificate, check_id=check_id or model_id or "")

    # ── Text AI ───────────────────────────────────────────────────────────────

    def text_summarize(self, text: str, **kwargs: Any) -> TextSummary:
        """/v1/text/summarize — 1-3 sentence extractive summary. $0.040/request"""
        return self._post_model("/v1/text/summarize", TextSummary, {"text": text, **kwargs})

    def text_keywords(self, text: str, top_k: int = 10, **kwargs: Any) -> TextKeywords:
        """/v1/text/keywords — TF-IDF keyword extraction. $0.020/request"""
        return self._post_model("/v1/text/keywords", TextKeywords, {"text": text, "top_k": top_k, **kwargs})

    def text_sentiment(self, text: str, **kwargs: Any) -> TextSentiment:
        """/v1/text/sentiment — positive / negative / neutral. $0.020/request"""
        return self._post_model("/v1/text/sentiment", TextSentiment, {"text": text, **kwargs})

    # ── Data Tools ────────────────────────────────────────────────────────────

    def data_validate_json(
        self,
        data: dict | None = None,
        schema: dict | None = None,
        *,
        payload: dict | None = None,
        **kwargs: Any,
    ) -> DataValidation:
        """/v1/data/validate-json — JSON schema validation with error paths. $0.012/request"""
        return self._post_model("/v1/data/validate-json", DataValidation, {"data": data or payload or {}, "schema": schema or {}, **kwargs})

    def data_format_convert(self, data: str, from_format: str, to_format: str, **kwargs: Any) -> FormatConversion:
        """/v1/data/format-convert — JSON ↔ CSV transformation. $0.020/request"""
        return self._post_model("/v1/data/format-convert", FormatConversion, {
            "data": data, "from_format": from_format, "to_format": to_format, **kwargs,
        })

    def data_convert(self, content: str, target_format: str, **kwargs: Any) -> dict:
        """/v1/data/convert — Convert text content to a target format. $0.020/request"""
        return self._post_raw("/v1/data/convert", {"content": content, "target_format": target_format, **kwargs})

    # ── Governance ────────────────────────────────────────────────────────────

    def governance_vote(self, agent_id: str, proposal_id: str, vote: str, weight: float = 1.0, **kwargs: Any) -> GovernanceVote:
        """/v1/governance/vote — on-chain governance vote (GOV-112). $0.040/call"""
        return self._post_model("/v1/governance/vote", GovernanceVote, {
            "agent_id": agent_id, "proposal_id": proposal_id, "vote": vote, "weight": weight, **kwargs,
        })

    def ethics_compliance(self, system_description: str, **kwargs: Any) -> EthicsCheckResult:
        """/v1/ethics/compliance — Prime Axiom audit with formal proof of safety. $0.040/call"""
        return self._post_model("/v1/ethics/compliance", EthicsCheckResult, {"system_description": system_description, **kwargs})

    # ── Advanced Platform / Billing ───────────────────────────────────────────

    def efficiency_capture(self, interactions: list[dict], **kwargs: Any) -> EfficiencyResult:
        """/v1/efficiency — ROI signal across agent interactions (PAY-506). $0.040/call"""
        return self._post_model("/v1/efficiency", EfficiencyResult, {"interactions": interactions, **kwargs})

    def billing_outcome(self, task_id: str, success: bool, metric_value: float, **kwargs: Any) -> BillingOutcome:
        """/v1/billing/outcome — pay only for measurably successful tasks (PAY-509). $0.040/call"""
        return self._post_model("/v1/billing/outcome", BillingOutcome, {
            "task_id": task_id, "success": success, "metric_value": metric_value, **kwargs,
        })

    def costs_attribute(self, run_id: str, **kwargs: Any) -> CostAttribution:
        """/v1/costs/attribute — token spend by agent/task/model (DEV-603). $0.040/call"""
        return self._post_model("/v1/costs/attribute", CostAttribution, {"run_id": run_id, **kwargs})

    def memory_trim(self, context: list[dict], target_tokens: int, **kwargs: Any) -> MemoryTrimResult:
        """/v1/memory/trim — prune context window for cost efficiency (INF-815). $0.040/call"""
        return self._post_model("/v1/memory/trim", MemoryTrimResult, {"context": context, "target_tokens": target_tokens, **kwargs})

    def routing_think(self, query: str, **kwargs: Any) -> ThinkRoute:
        """/v1/routing/think — classify complexity → model tier (POP-1207). $0.040/call"""
        return self._post_model("/v1/routing/think", ThinkRoute, {"query": query, **kwargs})

    def routing_recommend(self, task: str | None = None, *, prompt: str | None = None, **kwargs: Any) -> RoutingRecommend:
        """/v1/routing/recommend — map task to optimal model + routing tier. $0.020/call"""
        return self._post_model(
            "/v1/routing/recommend",
            RoutingRecommend,
            {"task": task or prompt or "", **kwargs},
        )

    # ── Developer Tools ───────────────────────────────────────────────────────

    def crypto_toolkit(self, data: str, **kwargs: Any) -> CryptoToolkit:
        """/v1/dcm/crypto-toolkit — BLAKE3 + Merkle proof + nonce (DCM-1018). $0.020/call"""
        return self._post_model("/v1/dcm/crypto-toolkit", CryptoToolkit, {"data": data, **kwargs})

    def dev_starter(self, project_name: str, language: str = "python", **kwargs: Any) -> StarterKit:
        """/v1/dev/starter — scaffold agent project with x402 wiring (DEV-601). $0.040/call"""
        return self._post_model("/v1/dev/starter", StarterKit, {"project_name": project_name, "language": language, **kwargs})

    def docs_generate(
        self,
        path_analysis: dict[str, Any],
        agent_id: str | None = None,
    ) -> DocsResult:
        """Generate documentation suite via AAAA-Nexus synthesis engine."""
        payload: dict[str, Any] = {"path_analysis": path_analysis}
        if agent_id:
            payload["agent_id"] = agent_id
        return self._post_model("/v1/docs/generate", DocsResult, payload)

    def lint_analyze(
        self,
        path_analysis: dict[str, Any],
        agent_id: str | None = None,
    ) -> LintResult:
        """Run monadic lint analysis via AAAA-Nexus synthesis engine."""
        payload: dict[str, Any] = {"path_analysis": path_analysis}
        if agent_id:
            payload["agent_id"] = agent_id
        return self._post_model("/v1/lint/analyze", LintResult, payload)

    def certify_codebase(
        self,
        local_certificate: dict[str, Any],
        agent_id: str | None = None,
    ) -> CertifyResult:
        """Sign and certify a codebase via AAAA-Nexus PQC signing."""
        payload: dict[str, Any] = {"certificate": local_certificate}
        if agent_id:
            payload["agent_id"] = agent_id
        return self._post_model("/v1/certify/codebase", CertifyResult, payload)

    def design_blueprint(
        self,
        description: str,
        context: dict[str, Any] | None = None,
        agent_id: str | None = None,
    ) -> DesignBlueprint:
        """Generate an AAAA-SPEC-004 blueprint from a natural language description."""
        payload: dict[str, Any] = {"description": description}
        if context:
            payload["context"] = context
        if agent_id:
            payload["agent_id"] = agent_id
        return self._post_model("/v1/uep/design", DesignBlueprint, payload)

    # ── BitNet 1.58-bit Inference ─────────────────────────────────────────────

    def bitnet_models(self, **kwargs: Any) -> BitNetModelsResponse:
        """GET /v1/bitnet/models — list available 1.58-bit models (BIT-102). Free."""
        return self._get_model("/v1/bitnet/models", BitNetModelsResponse, **kwargs)

    def bitnet_inference(self, prompt: str, model: str = "bitnet-b1.58-2B-4T", **kwargs: Any) -> BitNetInferenceResponse:
        """POST /v1/bitnet/inference — 1-bit chat completion (BIT-100). $0.020/call"""
        return self._post_model("/v1/bitnet/inference", BitNetInferenceResponse, {"prompt": prompt, "model": model, **kwargs})

    def bitnet_stream(self, prompt: str, model: str = "bitnet-b1.58-2B-4T", **kwargs: Any) -> Iterator[str]:
        """POST /v1/bitnet/inference/stream — streaming 1-bit CoT (BIT-101). $0.040/call"""
        with self._client.stream("POST", "/v1/bitnet/inference/stream", json={"prompt": prompt, "model": model, **kwargs}) as r:
            r.raise_for_status()
            for chunk in r.iter_text():
                if chunk:
                    yield chunk

    def bitnet_benchmark(self, model: str, n_tokens: int = 100, **kwargs: Any) -> BitNetBenchmarkResponse:
        """POST /v1/bitnet/benchmark — inference benchmark for a 1-bit model (BIT-103). $0.020/call"""
        return self._post_model("/v1/bitnet/benchmark", BitNetBenchmarkResponse, {"model": model, "n_tokens": n_tokens, **kwargs})

    def bitnet_quantize(self, model_id: str, **kwargs: Any) -> BitNetQuantizeResponse:
        """POST /v1/bitnet/quantize — convert model to 1.58-bit ternary weights (BIT-104). $0.100/call"""
        return self._post_model("/v1/bitnet/quantize", BitNetQuantizeResponse, {"model_id": model_id, **kwargs})

    def bitnet_status(self, **kwargs: Any) -> BitNetStatus:
        """GET /v1/bitnet/status — BitNet engine health and metrics (BIT-105). Free."""
        return self._get_model("/v1/bitnet/status", BitNetStatus, **kwargs)

    # ── VANGUARD ─────────────────────────────────────────────────────────────

    def vanguard_redteam(self, agent_id: str, target: str, **kwargs: Any) -> VanguardRedTeamResult:
        """POST /v1/vanguard/continuous-redteam — orchestrated red-team audit. $0.100/run"""
        return self._post_model("/v1/vanguard/continuous-redteam", VanguardRedTeamResult, {"agent_id": agent_id, "target": target, **kwargs})

    def vanguard_mev_route(self, agent_id: str, intent: dict | None = None, **kwargs: Any) -> VanguardMevRouteResult:
        """POST /v1/vanguard/mev/route-intent — MEV route governance. $0.040/call"""
        return self._post_model("/v1/vanguard/mev/route-intent", VanguardMevRouteResult, {"agent_id": agent_id, "intent": intent or {}, **kwargs})

    def vanguard_govern_session(self, agent_id: str, session_key: str | None = None, *, wallet: str | None = None, **kwargs: Any) -> VanguardSessionResult:
        """POST /v1/vanguard/wallet/govern-session — UCAN wallet session control. $0.040/call"""
        return self._post_model("/v1/vanguard/wallet/govern-session", VanguardSessionResult, {"agent_id": agent_id, "session_key": session_key or wallet or "", **kwargs})

    def vanguard_start_session(self, agent_id: str, **kwargs: Any) -> VanguardSessionResult:
        """POST /v1/vanguard/session/start — start a VANGUARD wallet session. $0.040/call"""
        return self._post_model("/v1/vanguard/session/start", VanguardSessionResult, {"agent_id": agent_id, **kwargs})

    def vanguard_lock_and_verify(
        self,
        payer_agent_id: str | None = None,
        payee_agent_id: str | None = None,
        amount_micro_usdc: int | None = None,
        *,
        agent_id: str | None = None,
        amount_usdc: float | None = None,
        **kwargs: Any,
    ) -> VanguardEscrowResult:
        """POST /v1/vanguard/escrow/lock-and-verify — lock + verify escrow (Vanguard). $0.040/call"""
        resolved_payer = payer_agent_id or agent_id or ""
        resolved_payee = payee_agent_id or agent_id or ""
        resolved_amount = amount_micro_usdc
        if resolved_amount is None:
            resolved_amount = int((amount_usdc or 0.0) * 1_000_000)
        return self._post_model("/v1/vanguard/escrow/lock-and-verify", VanguardEscrowResult, {
            "payer_agent_id": resolved_payer,
            "payee_agent_id": resolved_payee,
            "amount_micro_usdc": resolved_amount,
            **kwargs,
        })

    # ── MEV Shield ────────────────────────────────────────────────────────────

    def mev_protect(self, tx_bundle: list[str], **kwargs: Any) -> MevProtectResult:
        """POST /v1/mev/protect — MEV protection for a transaction bundle (MEV-100). $0.020/tx"""
        return self._post_model("/v1/mev/protect", MevProtectResult, {"tx_bundle": tx_bundle, **kwargs})

    def mev_status(self, bundle_id: str, **kwargs: Any) -> MevStatusResult:
        """GET /v1/mev/status — check MEV protection status for a bundle (MEV-101). Free."""
        return self._get_model("/v1/mev/status", MevStatusResult, bundle_id=bundle_id, **kwargs)

    # ── Forge Marketplace ─────────────────────────────────────────────────────

    def forge_leaderboard(self, **kwargs: Any) -> ForgeLeaderboardResponse:
        """GET /v1/forge/leaderboard — Forge agent leaderboard. Free."""
        return self._get_model("/v1/forge/leaderboard", ForgeLeaderboardResponse, **kwargs)

    def forge_verify(self, agent_id: str, **kwargs: Any) -> ForgeVerifyResult:
        """POST /v1/forge/verify — verify an agent for Forge badge. Free."""
        return self._post_model("/v1/forge/verify", ForgeVerifyResult, {"agent_id": agent_id, **kwargs})

    def forge_quarantine(self, model_id: str = "", reason: str = "probe", **kwargs: Any) -> ForgeQuarantineResponse:
        """POST /v1/forge/quarantine — quarantine a model. Free."""
        return self._post_model("/v1/forge/quarantine", ForgeQuarantineResponse, {"model_id": model_id, "reason": reason, **kwargs})

    def forge_delta_submit(self, agent_id: str, delta: dict, **kwargs: Any) -> ForgeDeltaSubmitResult:
        """POST /v1/forge/delta/submit — submit improvement delta. Free."""
        return self._post_model("/v1/forge/delta/submit", ForgeDeltaSubmitResult, {"agent_id": agent_id, "delta": delta, **kwargs})

    def forge_badge(self, badge_id: str, **kwargs: Any) -> ForgeBadgeResult:
        """GET /v1/forge/badge/{id} — retrieve Forge badge metadata. Free."""
        return self._get_model(f"/v1/forge/badge/{_pseg(badge_id, 'badge_id')}", ForgeBadgeResult, **kwargs)

    # ── LoRA federated-training endpoints ────────────────────────────────────

    def lora_contribute(
        self,
        samples: list[dict[str, Any]],
        *,
        agent_id: str | None = None,
        trust_floor_threshold: float | None = None,
        **kwargs: Any,
    ) -> dict[str, Any]:
        """POST /v1/lora/contribute — submit batch of privacy-scrubbed code fixes.

        Each sample: {digest, bad, good, lint_delta, language, size, ts}.
        Returns: {accepted, rejected, batch_size, agent_id, tau_threshold_used, reject_summary}.
        """
        payload: dict[str, Any] = {"samples": samples}
        if agent_id is not None:
            payload["agent_id"] = agent_id
        if trust_floor_threshold is not None:
            payload["trust_floor_threshold"] = trust_floor_threshold
        payload.update(kwargs)
        return self._post_raw("/v1/lora/contribute", payload)

    def lora_status(self, **kwargs: Any) -> dict[str, Any]:
        """GET /v1/lora/status — current training-run info."""
        return self._get_raw("/v1/lora/status", **kwargs)

    def lora_adapter_current(self, language: str = "python", **kwargs: Any) -> dict[str, Any]:
        """GET /v1/lora/adapter/{language} — latest adapter id for a language."""
        return self._get_raw(f"/v1/lora/adapter/{_pseg(language, 'language')}", **kwargs)

    def lora_reward_claim(
        self,
        agent_id: str | None = None,
        *,
        contribution_id: str | None = None,
        **kwargs: Any,
    ) -> dict[str, Any]:
        """POST /v1/lora/reward/claim — claim USDC payout for accepted samples."""
        payload: dict[str, Any] = {}
        if agent_id is not None:
            payload["agent_id"] = agent_id
        if contribution_id is not None:
            payload["contribution_id"] = contribution_id
        payload.update(kwargs)
        return self._post_raw("/v1/lora/reward/claim", payload)

    def lora_buffer_capture(
        self,
        bad: str,
        good: str,
        *,
        language: str = "python",
        lint_delta: float = 0.0,
        **kwargs: Any,
    ) -> dict[str, Any]:
        """POST /v1/lora/buffer/capture — stream a single (bad, good) pair to the training buffer.

        Preferred over lora_contribute() for single-sample streaming. The server
        batches samples internally and runs periodic training.
        """
        payload: dict[str, Any] = {
            "bad": bad,
            "good": good,
            "language": language,
            "lint_delta": lint_delta,
        }
        payload.update(kwargs)
        return self._post_raw("/v1/lora/buffer/capture", payload)

    def lora_buffer_inspect(self, **kwargs: Any) -> dict[str, Any]:
        """GET /v1/lora/buffer/inspect — show pending samples in the training buffer."""
        return self._get_raw("/v1/lora/buffer/inspect", **kwargs)

    def lora_credit_balance(self, agent_id: str | None = None, **kwargs: Any) -> dict[str, Any]:
        """GET /v1/lora/credit/balance — current Nexus credit balance for an agent.

        Returns: {agent_id, balance_micro_usdc, balance_usdc, reward_model}.
        """
        headers = {"X-Agent-Id": agent_id} if agent_id else {}
        if headers:
            # One-off header override; use the underlying client directly
            response = self._client.get("/v1/lora/credit/balance", headers=headers, params=kwargs)
        else:
            response = self._client.get("/v1/lora/credit/balance", params=kwargs)
        response.raise_for_status()
        return response.json()

    # Alias kept for compatibility with older callers (LoRAFlywheel)
    def lora_capture_fix(self, *args: Any, **kwargs: Any) -> dict[str, Any]:
        """Alias for lora_buffer_capture — single (bad, good) sample."""
        return self.lora_buffer_capture(*args, **kwargs)

    # ── Enhancement Engine ────────────────────────────────────────────────────

    def enhance_scan(
        self,
        local_report: dict[str, Any],
        agent_id: str | None = None,
    ) -> EnhanceScanResult:
        """Deep enhancement scan and blueprint generation via AAAA-Nexus."""
        payload: dict[str, Any] = {"local_report": local_report}
        if agent_id:
            payload["agent_id"] = agent_id
        return self._post_model("/v1/enhance/scan", EnhanceScanResult, payload)

    def enhance_apply(
        self,
        improvement_ids: list[int],
        local_report: dict[str, Any],
        agent_id: str | None = None,
    ) -> EnhanceApplyResult:
        """Apply selected enhancements: generate blueprints and trigger rebuild."""
        payload: dict[str, Any] = {
            "improvement_ids": improvement_ids,
            "local_report": local_report,
        }
        if agent_id:
            payload["agent_id"] = agent_id
        return self._post_model("/v1/enhance/apply", EnhanceApplyResult, payload)

    # ── Factory ───────────────────────────────────────────────────────────────

    @classmethod
    def resilient(
        cls,
        *,
        base_url: str,
        timeout: float = 20.0,
        api_key: str | None = None,
        max_retries: int = 3,
        circuit_failure_threshold: int = 5,
    ) -> NexusClient:
        """Create a client pre-configured with retry + circuit-breaker transports."""
        from ass_ade.nexus.resilience import build_resilient_transport

        transport = build_resilient_transport(
            max_retries=max_retries,
            circuit_failure_threshold=circuit_failure_threshold,
        )
        return cls(base_url=base_url, timeout=timeout, transport=transport, api_key=api_key)
