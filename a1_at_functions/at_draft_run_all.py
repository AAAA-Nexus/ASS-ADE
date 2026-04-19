# Extracted from C:/!ass-ade/scripts/probe_endpoints.py:83
# Component id: at.source.ass_ade.run_all
from __future__ import annotations

__version__ = "0.1.0"

def run_all(nx: NexusClient, only: str | None = None) -> None:

    def section(title: str) -> None:
        if only and only.lower() not in title.lower():
            return
        print(f"{CYAN}{'-' * 70}{RESET}")
        print(f"{CYAN}  {title}{RESET}")
        print(f"{CYAN}{'-' * 70}{RESET}")

    # ── Platform ──────────────────────────────────────────────────────────────
    section("platform")
    if not only or "platform" in only:
        probe("platform", "get_health",            lambda: nx.get_health())
        probe("platform", "get_openapi",           lambda: nx.get_openapi())
        probe("platform", "get_agent_card",        lambda: nx.get_agent_card())
        probe("platform", "get_mcp_manifest",      lambda: nx.get_mcp_manifest())
        probe("platform", "get_pricing_manifest",  lambda: nx.get_pricing_manifest())
        probe("platform", "get_payment_fee",       lambda: nx.get_payment_fee())
        probe("platform", "get_metrics",           lambda: nx.get_metrics())

    # ── Inference ─────────────────────────────────────────────────────────────
    section("inference")
    if not only or "inference" in only:
        probe("inference", "inference",         lambda: nx.inference("Say hello in one word."))
        probe("inference", "embed",             lambda: nx.embed([0.1, 0.2, 0.3]))
        probe("inference", "inference_stream",  lambda: list(nx.inference_stream("one word answer: 2+2?")))

    # ── Oracle ────────────────────────────────────────────────────────────────
    section("oracle")
    if not only or "oracle" in only:
        probe("oracle", "hallucination_oracle",  lambda: nx.hallucination_oracle("The sky is green."))
        probe("oracle", "trust_phase_oracle",    lambda: nx.trust_phase_oracle("test-agent-probe"))
        probe("oracle", "entropy_oracle",        lambda: nx.entropy_oracle())
        probe("oracle", "trust_decay",           lambda: nx.trust_decay("test-agent-probe", 5))

    # ── Ratchet ───────────────────────────────────────────────────────────────
    section("ratchet")
    if not only or "ratchet" in only:
        sess = None
        def _ratchet_flow() -> None:
            nonlocal sess
            sess = nx.ratchet_register(13608)  # G_18-sovereign agent (324 * 42)
        probe("ratchet", "ratchet_register",  _ratchet_flow)
        if sess:
            sid = sess.session_id  # type: ignore[attr-defined]
            probe("ratchet", "ratchet_advance",  lambda: nx.ratchet_advance(sid))
            probe("ratchet", "ratchet_probe",    lambda: nx.ratchet_probe([sid]))
            probe("ratchet", "ratchet_status",   lambda: nx.ratchet_status(sid))

    # ── RNG ───────────────────────────────────────────────────────────────────
    section("rng")
    if not only or "rng" in only:
        rng_r = None
        def _rng() -> None:
            nonlocal rng_r
            rng_r = nx.rng_quantum(3)
        probe("rng", "rng_quantum",  _rng)
        if rng_r:
            probe("rng", "rng_verify",  lambda: nx.rng_verify(
                rng_r.seed_ts,  # type: ignore[attr-defined]
                ",".join(str(n) for n in rng_r.numbers),  # type: ignore[attr-defined]
                rng_r.proof,  # type: ignore[attr-defined]
            ))

    # ── VRF ───────────────────────────────────────────────────────────────────
    section("vrf")
    if not only or "vrf" in only:
        draw_r = None
        def _vrf() -> None:
            nonlocal draw_r
            draw_r = nx.vrf_draw(1, 100, 3)
        probe("vrf", "vrf_draw",         _vrf)
        if draw_r:
            probe("vrf", "vrf_verify_draw",  lambda: nx.vrf_verify_draw(draw_r.draw_id))  # type: ignore[attr-defined]

    # ── Identity ──────────────────────────────────────────────────────────────
    section("identity")
    if not only or "identity" in only:
        probe("identity", "identity_verify",   lambda: nx.identity_verify("probe-actor"))
        probe("identity", "sybil_check",       lambda: nx.sybil_check("probe-actor"))
        probe("identity", "zero_trust_auth",   lambda: nx.zero_trust_auth(13608, "/v1/inference", "inference", 0.9984))
        probe("identity", "delegate_verify",   lambda: nx.delegate_verify([{"issuer": "a", "delegate": "b", "action": "read"}]))
        probe("identity", "delegation_validate", lambda: nx.delegation_validate([{"issuer": "a", "delegate": "b", "action": "read"}]))

    # ── Escrow ────────────────────────────────────────────────────────────────
    section("escrow")
    if not only or "escrow" in only:
        esc = None
        def _create_escrow() -> None:
            nonlocal esc
            esc = nx.escrow_create(1.0, "probe-payer", "probe-payee", ["task_completed"])
        probe("escrow", "escrow_create",  _create_escrow)
        if esc:
            eid = esc.escrow_id  # type: ignore[attr-defined]
            probe("escrow", "escrow_status",   lambda: nx.escrow_status(eid))
            probe("escrow", "escrow_dispute",  lambda: nx.escrow_dispute(eid, "probe test dispute"))

    # ── Reputation ────────────────────────────────────────────────────────────
    section("reputation")
    if not only or "reputation" in only:
        probe("reputation", "reputation_record",   lambda: nx.reputation_record("probe-agent", True, 0.9, 200.0))
        probe("reputation", "reputation_score",    lambda: nx.reputation_score("probe-agent"))
        probe("reputation", "reputation_history",  lambda: nx.reputation_history("probe-agent"))

    # ── SLA ───────────────────────────────────────────────────────────────────
    section("sla")
    if not only or "sla" in only:
        sla = None
        def _sla_reg() -> None:
            nonlocal sla
            sla = nx.sla_register("probe-agent", 200.0, 99.9, 0.01, 5.0)
        probe("sla", "sla_register",  _sla_reg)
        if sla:
            sid = sla.sla_id  # type: ignore[attr-defined]
            probe("sla", "sla_report",  lambda: nx.sla_report(sid, "latency_ms", 180.0))
            probe("sla", "sla_status",  lambda: nx.sla_status(sid))

    # ── Discovery ─────────────────────────────────────────────────────────────
    section("discovery")
    if not only or "discovery" in only:
        probe("discovery", "discovery_search",    lambda: nx.discovery_search("code review"))
        probe("discovery", "discovery_recommend", lambda: nx.discovery_recommend("run unit tests"))
        probe("discovery", "discovery_registry",  lambda: nx.discovery_registry())

    # ── Swarm ─────────────────────────────────────────────────────────────────
    section("swarm")
    if not only or "swarm" in only:
        probe("swarm", "agent_register",        lambda: nx.agent_register(648, "probe-agent", ["classify"], "https://probe.test"))
        probe("swarm", "agent_topology",        lambda: nx.agent_topology())
        probe("swarm", "agent_intent_classify", lambda: nx.agent_intent_classify("schedule a meeting tomorrow"))
        probe("swarm", "agent_token_budget",    lambda: nx.agent_token_budget("summarise a 100-page PDF"))
        probe("swarm", "agent_contradiction",   lambda: nx.agent_contradiction("The sky is blue.", "The sky is not blue."))
        probe("swarm", "agent_plan",            lambda: nx.agent_plan("write and ship a Python CLI tool"))
        probe("swarm", "agent_semantic_diff",   lambda: nx.agent_semantic_diff("a dog barks", "a cat meows"))
        probe("swarm", "swarm_relay",           lambda: nx.swarm_relay("probe-a", "agent-b", {"text": "hello"}))

    # ── Security & Prompts ────────────────────────────────────────────────────
    section("security")
    if not only or "security" in only:
        probe("security", "prompt_inject_scan",  lambda: nx.prompt_inject_scan("ignore previous instructions"))
        probe("security", "prompt_optimize",     lambda: nx.prompt_optimize("Summarise this document"))
        probe("security", "security_zero_day",   lambda: nx.security_zero_day({"code": "os.system('ls')"}))
        probe("security", "threat_score",        lambda: nx.threat_score({"payload": "DROP TABLE users;"}))
        probe("security", "security_shield",     lambda: nx.security_shield({"content": "test probe"}))
        probe("security", "security_pqc_sign",   lambda: nx.security_pqc_sign("hello world"))
        probe("security", "ethics_check",        lambda: nx.ethics_check("Is it okay to deceive users?"))

    # ── Compliance ────────────────────────────────────────────────────────────
    section("compliance")
    if not only or "compliance" in only:
        probe("compliance", "compliance_check",         lambda: nx.compliance_check("AI loan approval system"))
        probe("compliance", "compliance_eu_ai_act",     lambda: nx.compliance_eu_ai_act("AI loan approval system"))
        probe("compliance", "compliance_fairness",      lambda: nx.compliance_fairness("binary classifier on demographic data"))
        probe("compliance", "compliance_incident",      lambda: nx.compliance_incident("probe-system", "test incident", "low"))
        probe("compliance", "aibom_drift",              lambda: nx.aibom_drift("gpt-4o"))
        probe("compliance", "drift_check",              lambda: nx.drift_check("gpt-4o", {"samples": [0.1]}, {"samples": [0.2]}))
        probe("compliance", "audit_log",                lambda: nx.audit_log({"event": "probe", "actor": "probe-agent"}))
        probe("compliance", "audit_verify",             lambda: nx.audit_verify())

    # ── DeFi ──────────────────────────────────────────────────────────────────
    section("defi")
    if not only or "defi" in only:
        probe("defi", "defi_optimize",          lambda: nx.defi_optimize("aave", 10000.0))
        probe("defi", "defi_risk_score",        lambda: nx.defi_risk_score("aave", {"collateral": 15000, "debt": 10000}))
        probe("defi", "defi_oracle_verify",     lambda: nx.defi_oracle_verify("uniswap-v3-eth-usdc", 500_000.0))
        probe("defi", "defi_liquidation_check", lambda: nx.defi_liquidation_check({"collateral": 15000, "debt": 10000}))
        probe("defi", "defi_bridge_verify",     lambda: nx.defi_bridge_verify("stargate", 5000.0))
        probe("defi", "defi_yield_optimize",    lambda: nx.defi_yield_optimize(10000.0, ["aave", "compound"]))

    # ── AEGIS ─────────────────────────────────────────────────────────────────
    section("aegis")
    if not only or "aegis" in only:
        probe("aegis", "aegis_mcp_proxy",        lambda: nx.aegis_mcp_proxy("hallucination-oracle", "probe test text", agent_id="13608"))
        probe("aegis", "aegis_epistemic_route",  lambda: nx.aegis_epistemic_route("What is 2 + 2?"))
        probe("aegis", "aegis_certify_epoch",    lambda: nx.aegis_certify_epoch("probe-system"))

    # ── Control / Authorization ────────────────────────────────────────────────
    section("control")
    if not only or "control" in only:
        probe("control", "authorize_action",    lambda: nx.authorize_action("probe-agent", "read:data", 0))
        probe("control", "spending_authorize",  lambda: nx.spending_authorize("probe-agent", 5.0, 1))
        probe("control", "spending_budget",     lambda: nx.spending_budget([{"agent": "probe", "budget": 5.0}], 5.0))
        probe("control", "lineage_record",      lambda: nx.lineage_record("probe goal", ["no harm"], "success"))
        probe("control", "agent_quarantine",    lambda: nx.agent_quarantine("probe-bad-agent", "probe test"))

    # ── Consensus ─────────────────────────────────────────────────────────────
    section("consensus")
    if not only or "consensus" in only:
        cs = None
        def _cs_create() -> None:
            nonlocal cs
            cs = nx.consensus_create("majority", ["agent-a", "agent-b", "agent-c"])
        probe("consensus", "consensus_create",  _cs_create)
        if cs:
            csid = cs.session_id  # type: ignore[attr-defined]
            probe("consensus", "consensus_vote",    lambda: nx.consensus_vote(csid, "agent-a", "abc123", 0.9))
            probe("consensus", "consensus_result",  lambda: nx.consensus_result(csid))

    # ── Quota ─────────────────────────────────────────────────────────────────
    section("quota")
    if not only or "quota" in only:
        qt = None
        def _qt_create() -> None:
            nonlocal qt
            qt = nx.quota_create(10000, [{"id": "child-1", "share": 0.5}, {"id": "child-2", "share": 0.5}])
        probe("quota", "quota_create",  _qt_create)
        if qt:
            qtid = qt.tree_id  # type: ignore[attr-defined]
            probe("quota", "quota_draw",    lambda: nx.quota_draw(qtid, "child-1", 100, "probe-idem-1"))
            probe("quota", "quota_status",  lambda: nx.quota_status(qtid))

    # ── Federation ────────────────────────────────────────────────────────────
    section("federation")
    if not only or "federation" in only:
        probe("federation", "federation_mint",        lambda: nx.federation_mint({"agent_id": "probe"}, ["openai", "anthropic"]))
        probe("federation", "federation_portability", lambda: nx.federation_portability("openai", "anthropic"))

    # ── Contract ──────────────────────────────────────────────────────────────
    section("contract")
    if not only or "contract" in only:
        probe("contract", "contract_verify",  lambda: nx.contract_verify({"id": "c1", "constraints": ["no harm"]}))

    # ── Saga ──────────────────────────────────────────────────────────────────
    section("saga")
    if not only or "saga" in only:
        saga = None
        def _saga_create() -> None:
            nonlocal saga
            saga = nx.saga_create("probe-saga", ["step-1", "step-2"], {"step-2": "undo-step-2"})
        probe("saga", "saga_create",  _saga_create)
        if saga:
            sgid = saga.saga_id  # type: ignore[attr-defined]
            probe("saga", "saga_checkpoint",  lambda: nx.saga_checkpoint(sgid, "step-1"))
            probe("saga", "saga_compensate",  lambda: nx.saga_compensate(sgid))

    # ── Memory fence ──────────────────────────────────────────────────────────
    section("memory")
    if not only or "memory" in only:
        fence = None
        def _fence_create() -> None:
            nonlocal fence
            fence = nx.memory_fence_create("probe-ns")
        probe("memory", "memory_fence_create",  _fence_create)
        if fence:
            probe("memory", "memory_fence_audit",  lambda: nx.memory_fence_audit(fence.fence_id))  # type: ignore[attr-defined]
        probe("memory", "memory_trim",  lambda: nx.memory_trim([{"role": "user", "content": "hi"}], 100))

    # ── Certify ───────────────────────────────────────────────────────────────
    section("certify")
    if not only or "certify" in only:
        cert = None
        def _certify() -> None:
            nonlocal cert
            cert = nx.certify_output("The answer is 42.", ["factually grounded", "concise"])
        probe("certify", "certify_output",  _certify)
        if cert:
            probe("certify", "certify_output_verify",  lambda: nx.certify_output_verify(cert.certificate_id))  # type: ignore[attr-defined]

    # ── Text AI ───────────────────────────────────────────────────────────────
    section("text")
    if not only or "text" in only:
        probe("text", "text_summarize",  lambda: nx.text_summarize("The quick brown fox jumps over the lazy dog repeatedly."))
        probe("text", "text_keywords",   lambda: nx.text_keywords("Machine learning is a subset of artificial intelligence.", 5))
        probe("text", "text_sentiment",  lambda: nx.text_sentiment("I absolutely love this product!"))

    # ── Data Tools ────────────────────────────────────────────────────────────
    section("data")
    if not only or "data" in only:
        probe("data", "data_validate_json",  lambda: nx.data_validate_json(
            {"name": "probe", "value": 42},
            {"type": "object", "properties": {"name": {"type": "string"}, "value": {"type": "integer"}}},
        ))
        probe("data", "data_format_convert",  lambda: nx.data_format_convert(
            '[{"id":1,"name":"probe"}]', "json", "csv",
        ))

    # ── Governance & Ethics ───────────────────────────────────────────────────
    section("governance")
    if not only or "governance" in only:
        probe("governance", "governance_vote",    lambda: nx.governance_vote("probe-agent", "proposal-1", "yes", 1.0))
        probe("governance", "ethics_compliance",  lambda: nx.ethics_compliance("autonomous drone system"))

    # ── Billing / Efficiency ──────────────────────────────────────────────────
    section("billing")
    if not only or "billing" in only:
        probe("billing", "efficiency_capture",  lambda: nx.efficiency_capture([{"agent": "probe", "tokens": 100, "outcome": "success"}]))
        probe("billing", "billing_outcome",     lambda: nx.billing_outcome("task-probe-1", True, 0.95))
        probe("billing", "costs_attribute",     lambda: nx.costs_attribute("run-probe-1"))
        probe("billing", "routing_think",       lambda: nx.routing_think("explain quantum entanglement"))
        probe("billing", "routing_recommend",   lambda: nx.routing_recommend("summarise 50-page PDF"))

    # ── Dev Tools ─────────────────────────────────────────────────────────────
    section("dev")
    if not only or "dev" in only:
        probe("dev", "dev_starter",    lambda: nx.dev_starter("probe-project"))
        probe("dev", "crypto_toolkit", lambda: nx.crypto_toolkit("hello probe"))

    # ── Trust ─────────────────────────────────────────────────────────────────
    section("trust")
    if not only or "trust" in only:
        probe("trust", "trust_score",    lambda: nx.trust_score("probe-agent"))
        probe("trust", "trust_history",  lambda: nx.trust_history("probe-agent"))

    # ── BitNet ────────────────────────────────────────────────────────────────
    section("bitnet")
    if not only or "bitnet" in only:
        probe("bitnet", "bitnet_status",    lambda: nx.bitnet_status())
        probe("bitnet", "bitnet_models",    lambda: nx.bitnet_models())
        probe("bitnet", "bitnet_inference", lambda: nx.bitnet_inference("Reply with one word: hello", "bitnet-b1.58-2B-4T"))
        probe("bitnet", "bitnet_benchmark", lambda: nx.bitnet_benchmark("bitnet-b1.58-2B-4T", 20))
        probe("bitnet", "bitnet_stream",    lambda: list(nx.bitnet_stream("one word answer: 2+2?")))

    # ── Vanguard ──────────────────────────────────────────────────────────────
    section("vanguard")
    if not only or "vanguard" in only:
        probe("vanguard", "vanguard_redteam",        lambda: nx.vanguard_redteam("probe-agent", "probe-system"))
        probe("vanguard", "vanguard_mev_route",      lambda: nx.vanguard_mev_route("probe-agent", {"action": "swap"}))
        probe("vanguard", "vanguard_govern_session", lambda: nx.vanguard_govern_session("probe-agent", "0xProbeWallet"))
        probe("vanguard", "vanguard_lock_and_verify", lambda: nx.vanguard_lock_and_verify("probe-agent", "probe-payee", 1000))

    # ── MEV Shield ────────────────────────────────────────────────────────────
    section("mev")
    if not only or "mev" in only:
        mev_r = None
        def _mev_protect() -> None:
            nonlocal mev_r
            mev_r = nx.mev_protect(["0xaaaaaa", "0xbbbbbb"])
        probe("mev", "mev_protect",  _mev_protect)
        if mev_r:
            probe("mev", "mev_status",  lambda: nx.mev_status(mev_r.bundle_id))  # type: ignore[attr-defined]

    # ── Forge ─────────────────────────────────────────────────────────────────
    section("forge")
    if not only or "forge" in only:
        probe("forge", "forge_leaderboard",  lambda: nx.forge_leaderboard())
        probe("forge", "forge_verify",       lambda: nx.forge_verify("probe-agent"))
        probe("forge", "forge_quarantine",   lambda: nx.forge_quarantine("probe-model-v1", "safety-violation"))
        probe("forge", "forge_delta_submit", lambda: nx.forge_delta_submit("probe-agent", {"improvement": "added retry"}))
