# Extracted from C:/!ass-ade/.claude/worktrees/adoring-boyd-0e3a8f/src/ass_ade/nexus/client.py:202
# Component id: mo.source.ass_ade.nexusclient
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
        