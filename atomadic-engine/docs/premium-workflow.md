# ASS-ADE Premium Workflow Baseline

**Status:** Blueprint v1.0 — synthesis of AAAA-Nexus-MCP 140-tool catalog, UEP v17.5 gate order, and ASS-ADE tier strategy.

---

## 1. The Three Modes

| Mode | What runs | Cost |
|------|-----------|------|
| **Local** | 14 built-in MCP tools, no network required | Free |
| **Hybrid** | Local tools + free-tier AAAA-Nexus endpoints | Free (metered) |
| **Premium** | Full AAAA-Nexus 140-tool surface, UEP-grade gates | Pay-per-call (USDC) |

---

## 2. Full AAAA-Nexus Tool Catalog — Tier Classification

### 2.1 Free (no key, always available)

| Tool | Endpoint | What it does |
|------|----------|-------------|
| `nexus_health` | `GET /health` | API liveness |
| `nexus_metrics` | `GET /v1/metrics` | Platform telemetry |
| `nexus_pricing` | `GET /v1/pricing` | Live price manifest |
| `nexus_agent_card` | `GET /v1/agent/card` | A2A capability manifest |
| `nexus_agent_register` | `POST /v1/agents/register` | Register agent identity |
| `nexus_rng_verify` | included | Verify quantum draw |
| `nexus_sys_constants` | local | Sovereign invariants (local compute) |
| `nexus_lora_capture_fix` | local | Capture bug/fix pair for training buffer |
| `nexus_lora_buffer_inspect` | local | Inspect local training buffer |
| `nexus_lora_buffer_clear` | local | Clear local training buffer |

### 2.2 Trial Bucket A — Low friction, high signal (< $0.020/call)

Good for ambient telemetry and session hygiene. Give 100 calls/day free-tier.

| Tool | Price | Purpose |
|------|-------|---------|
| `nexus_entropy_oracle` | $0.004 | Epistemic uncertainty measurement |
| `nexus_trust_decay` | $0.008 | Track trust degradation over time |
| `nexus_ratchet_status` | $0.004 | Check epoch ratchet state |
| `nexus_ratchet_register` | $0.008 | Initialize ratchet session |
| `nexus_ratchet_advance` | $0.008 | Advance epoch, lock trace |
| `nexus_ratchet_probe` | $0.008 | Non-destructive epoch probe |
| `nexus_delegation_depth` | $0.005 | Check delegation chain depth |
| `nexus_session_ratchet` | $0.010 | Per-session epoch pin |
| `nexus_friction_score` | $0.010 | Cost-of-variation check |
| `nexus_agent_topology` | $0.008 | Live swarm topology |
| `nexus_escrow_status` | $0.008 | Check escrow state |
| `nexus_reputation_score` | $0.008 | Agent reputation score |
| `nexus_sla_status` | $0.008 | SLA contract status |
| `nexus_rng_quantum` | $0.020 | Quantum-sourced random |
| `nexus_lora_status` | $0.005 | LoRA adapter status |
| `nexus_lora_contribute` | $0.010 | Submit training samples → earn rebates |
| `nexus_vrf_draw` | $0.010 + 0.5% | Verifiable random function draw |

### 2.3 Trial Bucket B — Reasoning primitives ($0.020–$0.040/call)

Mid-tier cognitive tools. Give 50 calls/day on trial key.

| Tool | Price | Purpose |
|------|-------|---------|
| `nexus_trust_phase` | $0.020 | V-AI phase transition oracle |
| `nexus_chain_parity` | $0.020 | Checksum the tool call chain |
| `nexus_payload_decompose` | $0.020 | Structural integrity of outputs |
| `nexus_novelty_jump` | $0.030 | Detect phase transitions in reasoning |
| `nexus_variant_rotate` | $0.040 | Rotate candidate variant set |
| `nexus_fuel_budget_spend` | $0.010 | Burn from fuel budget |
| `nexus_fuel_budget_create` | $0.040 | Create fuel budget for session |
| `nexus_vq_memory_query` | $0.010 | Vector-quantized memory lookup |
| `nexus_vq_memory_store` | $0.020 | Store to VQ memory |
| `nexus_agent_intent_classify` | $0.020 | Classify agent intent |
| `nexus_agent_token_budget` | $0.020 | Token budget negotiation |
| `nexus_agent_contradiction` | $0.020 | Detect reasoning contradictions |
| `nexus_routing_recommend` | $0.020 | Model routing recommendation |
| `nexus_routing_think` | $0.040 | Deep routing analysis |
| `nexus_text_keywords` | $0.020 | Keyword extraction |
| `nexus_text_sentiment` | $0.020 | Sentiment scoring |
| `nexus_pqc_sign` | $0.020 | Post-quantum signing |
| `nexus_reputation_record` | $0.020 | Record reputation event |
| `nexus_reputation_history` | $0.012 | Agent reputation history |
| `nexus_compliance_oversight` | $0.020 | Human oversight compliance check |
| `nexus_compliance_incident` | $0.020 | Incident registry |
| `nexus_lora_adapter_current` | $0.010 | Pull current community LoRA adapter |
| `nexus_lora_reward_claim` | $0.020 | Claim training reward |
| `nexus_consensus_vote` | $0.020 | Vote in consensus session |
| `nexus_consensus_result` | $0.020 | Read consensus result |
| `nexus_quota_draw` | $0.020 | Draw from quota tree |
| `nexus_quota_status` | $0.020 | Quota tree status |
| `nexus_sla_report` | $0.020 | SLA performance report |
| `nexus_escrow_release` | $0.020 | Release escrow on outcome |
| `nexus_discovery_registry` | $0.020 | Browse tool registry |

### 2.4 Trial Bucket C — Premium gates ($0.040–$0.060/call)

Core premium surface. No free calls — paid key required.

| Tool | Price | Purpose |
|------|-------|---------|
| `nexus_trust_gate` | $0.060 | Sovereign confidence gate (τ threshold) |
| `nexus_lint_gate` | $0.040 | Lint score ≥ 0.95 enforcement |
| `nexus_hallucination_oracle` | $0.040 | Hallucination probability verdict |
| `nexus_trust_score` | $0.040 | Full trust scoring |
| `nexus_trust_history` | $0.040 | Trust trajectory over time |
| `nexus_prompt_inject_scan` | $0.040 | Injection attack detection |
| `nexus_prompt_optimize` | $0.040 | Prompt improvement optimization |
| `nexus_security_prompt_scan` | $0.040 | Deep prompt security scan |
| `nexus_threat_score` | $0.040 | Threat model scoring |
| `nexus_security_shield` | $0.040 | Active security shielding |
| `nexus_zero_day_scan` | $0.040 | Zero-day pattern detection |
| `nexus_ethics_check` | $0.040 | Ethics compliance verdict |
| `nexus_compliance_check` | $0.040 | General compliance check |
| `nexus_compliance_eu_ai_act` | $0.040 | EU AI Act Annex IV gating |
| `nexus_compliance_fairness` | $0.040 | Fairness audit |
| `nexus_compliance_explain` | $0.040 | GDPR Art. 22 explainability |
| `nexus_compliance_lineage` | $0.040 | Data lineage compliance |
| `nexus_compliance_transparency` | $0.040 | Transparency report |
| `nexus_compliance_aibom_drift` | — | AI bill-of-materials drift |
| `nexus_compliance_drift_check` | — | Drift detection |
| `nexus_compliance_drift_certificate` | — | Drift compliance certificate |
| `nexus_compliance_memory_fence_create` | — | Memory isolation fence |
| `nexus_compliance_memory_fence_audit` | — | Memory fence audit |
| `nexus_certify_output` | — | Output certification |
| `nexus_certify_output_verify` | — | Verify certified output |
| `nexus_lineage_record` | $0.020 | Tamper-evident lineage receipt |
| `nexus_lineage_trace` | — | Full lineage trace |
| `nexus_agent_semantic_diff` | $0.040 | Semantic diff between versions |
| `nexus_agent_reputation` | $0.040 | Agent reputation composite |
| `nexus_agent_plan` | $0.060 | Dependency-aware step DAG |
| `nexus_inference` | $0.060 | Premium LLM inference |
| `nexus_embed` | $0.040 | Embedding with provenance |
| `nexus_text_summarize` | $0.040 | Provenance-chained summary |
| `nexus_memory_trim` | $0.040 | Adversarial memory pruning |
| `nexus_aegis_mcp_proxy` | $0.040 | AEGIS MCP proxy execution |
| `nexus_aegis_epistemic_route` | $0.040 | Epistemic routing with bounds |
| `nexus_aegis_certify_epoch` | $0.060 | Epoch certification (compliance capstone) |
| `nexus_escrow_create` | $0.040 | Create outcome-based escrow |
| `nexus_escrow_dispute` | $0.060 | Escalate escrow dispute |
| `nexus_consensus_create` | $0.040 | Open consensus session |
| `nexus_quota_create` | $0.040 | Create hierarchical quota tree |
| `nexus_discovery_search` | $0.060 | Federated tool/agent search |
| `nexus_discovery_recommend` | $0.040 | Discovery recommendation |
| `nexus_authorize_action` | $0.040 | Action authorization gate |
| `nexus_spending_authorize` | $0.040 | Spending authorization |
| `nexus_spending_budget` | $0.040 | Budget allocation |
| `nexus_sla_breach` | $0.040 | Report SLA breach |
| `nexus_sla_register` | $0.080 | Register SLA contract |
| `nexus_vanguard_mev_route` | $0.040 | MEV-resistant routing |
| `nexus_vanguard_govern_session` | $0.040 | Wallet governance session |
| `nexus_vanguard_lock_verify` | $0.040 | Wallet lock verification |

### 2.5 Enterprise — Continuous assurance (highest tier)

| Tool | Price | Purpose |
|------|-------|---------|
| `nexus_vanguard_redteam` | $0.100 | Continuous adversarial red-team |
| `nexus_reputation_dispute` | $0.080 | Dispute agent reputation record |
| `nexus_agent_capabilities_match` | — | Agent-to-task capability matching |
| `nexus_swarm_inbox` | — | Swarm message inbox |
| `nexus_swarm_relay` | — | Cross-swarm relay |

---

## 3. The Premium UEP-Grade Workflow

This is the full 9-phase execution loop that ASS-ADE exposes when a paid key is present.
Locally degraded variants exist for each phase (shown as fallback).

```
Phase 0 — Session bootstrap
  nexus_session_ratchet        pin epoch
  nexus_fuel_budget_create     allocate token budget
  phase0_recon                 Never Code Blind repo recon + source targets
  context_pack                 hash relevant files and source URLs into packet
  context_memory_query         recall local vector task memory

Phase 1 — Pre-task gates  [UEP: NCB + integrity axiom + G23]
  nexus_friction_score         cost-of-variation check
  nexus_trust_gate             confidence ≥ τ or abstain
  nexus_agent_plan             dependency-aware step DAG
  nexus_routing_think          pick model tier
  nexus_trusted_rag_augment    premium provenance-bearing context
  nexus_vq_memory_store        store task archetype and novelty baseline

Phase 2 — Context preparation  [UEP: TCA engine]
  map_terrain / nexus_map_terrain
                              verify required agents/hooks/skills/tools/harnesses exist
  nexus_embed                  embed context with provenance
  nexus_vq_memory_query        recall relevant VQ memory
  nexus_hallucination_oracle   gate retrieved context

Phase 3 — Synthesis  [UEP: CIE + SAM engines]
  nexus_routing_recommend      confirm model selection
  nexus_inference              premium inference with lineage
  nexus_prompt_optimize        improve prompt before execution

Phase 4 — Security scan  [UEP: hardness gate]
  nexus_prompt_inject_scan     injection attack detection
  nexus_security_shield        active shielding
  nexus_threat_score           threat model verdict

Phase 5 — Verification  [UEP: post-synthesis verification]
  nexus_lint_gate              lint score ≥ 0.95
  nexus_chain_parity           checksum tool call chain
  nexus_payload_decompose      structural integrity
  nexus_novelty_jump           flag phase transitions

Phase 6 — Compliance  [UEP: WisdomEngine]
  nexus_compliance_check       base compliance
  nexus_ethics_check           ethics verdict
  nexus_compliance_eu_ai_act   EU AI Act Annex IV  [enterprise]
  nexus_certify_output         output certification

Phase 7 — Post-task telemetry  [UEP: EDEE trace capture]
  nexus_lora_capture_fix       buffer fix pair for training
  nexus_trust_score            update trust trajectory
  nexus_lineage_record         tamper-evident receipt
  nexus_reputation_record      record agent performance
  nexus_ratchet_advance        advance epoch, lock trace

Phase 8 — Learning loop  [UEP: BAS breakthrough detection]
  nexus_lora_contribute        submit to shared training pool
  nexus_lora_reward_claim      claim reputation rebate
  nexus_novelty_jump           detect capability jumps
```

---

## 4. Free-Tier Degraded Variants

When no paid key is present, ASS-ADE falls back to these local equivalents:

| Premium Phase | Local Fallback |
|--------------|----------------|
| trust_gate | `gates.py` ECE-based confidence check |
| agent_plan | `local/planner.py` dependency-free plan |
| routing_think | `engine/router.py` static model selection |
| phase0_recon | Local repo recon plus required source target list |
| trusted_rag_augment | `context_pack` with repo excerpts and source URLs |
| embed / vq_memory | `context_memory_store` / `context_memory_query` local vector memory |
| hallucination_oracle | No gate; user warning emitted |
| lint_gate | `ruff` local lint check |
| chain_parity | Local hash of tool call log |
| compliance_check | Static checklist (no live scoring) |
| lineage_record | Local JSON append-only log |
| lora_capture_fix | Buffer stored locally only (no contribution) |
| inference | Local LLM via ollama / LM Studio |

---

## 5. Tier Bucket Definitions

Based on daily call volume and use-case profile:

| Bucket | Daily calls | Key required | Primary tools | Target user |
|--------|------------|--------------|---------------|-------------|
| **Free** | Unlimited | No | health, metrics, agent_card, local tools | Evaluation |
| **Trial-A** | 100 | Trial key (email) | Bucket A (< $0.020) | Curious devs |
| **Trial-B** | 50 | Trial key | Bucket A+B | Active builders |
| **Starter** | 500 | Paid key ($10/mo) | Buckets A+B+C | Pro individuals |
| **Pro** | 5000 | Paid key ($50/mo) | Full catalog | Teams |
| **Enterprise** | Unlimited | Custom | Full + VANGUARD + SLA | Orgs |

---

## 6. Workflow Integration Points

### 6.1 ASS-ADE MCP server changes needed (from Internal MCP audit)

Before premium workflow can be wired, these blockers must be fixed:

1. **CRITICAL** — Add stdin size limit (`MAX_REQUEST_BYTES = 65536`) before JSON parse
2. **CRITICAL** — Replace single-threaded loop with `asyncio` to support real cancellation
3. **CRITICAL** — Add per-tool billing ceiling validation before any Nexus call
4. **HIGH** — Enforce `_initialized` flag at request entry point
5. **HIGH** — Strip exception detail from client error responses
6. **HIGH** — Replace synchronous Nexus calls with `async/await`
7. **MEDIUM** — Add write lock to prevent interleaved JSON-RPC responses
8. **MEDIUM** — Replace hardcoded 14-tool list with dynamic tool injection from Nexus
9. **MEDIUM** — Add `resources` capability for premium certificates/receipts
10. **MEDIUM** — Add proper `safe_execute` payload validation before tool dispatch

### 6.2 Dynamic Nexus tool injection

When a paid key is present, the MCP server should dynamically register the 140 AAAA-Nexus tools alongside the 14 local tools. This requires:

- On `initialize`: call `nexus_pricing` to fetch available tools for the key's tier
- Synthesize tool descriptors compatible with MCP `tools/list` response
- Route `tools/call` requests matching `nexus_*` prefix through the AAAA-Nexus client

### 6.3 ASS-ADE aggregating server target architecture

```
Claude Desktop / VS Code Copilot
         │ JSON-RPC 2.0 stdio
         ▼
┌─────────────────────────────────────┐
│         ASS-ADE MCP Server          │
│  tools/list = local(14) + nexus(140)│
│  tools/call dispatcher              │
│    └── local_*  → local handlers   │
│    └── nexus_*  → NexusClient.post │
└─────────────────────────────────────┘
         │ HTTPS
         ▼
   atomadic.tech/v1/*
   (AAAA-Nexus backend)
```

---

## 7. Premium Workflow Cost Estimates

Full premium loop (Phases 0–8, all 9 phases once):

| Phase | Tools called | Est. cost |
|-------|-------------|-----------|
| Session bootstrap | ratchet + budget | $0.050 |
| Pre-task gates | friction + trust_gate + plan + routing | $0.150 |
| Context prep | embed + vq_query + hallucination | $0.110 |
| Synthesis | routing_recommend + inference + prompt_opt | $0.140 |
| Security scan | inject_scan + shield + threat | $0.120 |
| Verification | lint + chain_parity + payload + novelty | $0.110 |
| Compliance | compliance + ethics + certify | $0.120 |
| Post-task telemetry | lora_capture + trust_score + lineage + reputation + ratchet | $0.118 |
| Learning loop | lora_contribute + reward_claim + novelty | $0.060 |
| **Total (one full cycle)** | | **~$0.98** |

Cost per 1000 full premium cycles: **~$980**.

Revenue at $50/mo Pro tier with 5000 cycles/day: margin positive after ~2 Pro subscribers per infra unit.

---

## 8. Next Implementation Steps

### Immediate (unblocks premium wiring)

1. Fix 10 MCP server blockers from Internal MCP audit (see §6.1)
2. Implement `asyncio`-based server loop in `src/ass_ade/mcp/server.py`
3. Add `NexusClient` import and wiring in `src/ass_ade/mcp/server.py`
4. Implement dynamic tool injection from `nexus_pricing` on `initialize`

### Short-term (premium experience)

5. Wire Phase 1 (pre-task gates) into `agent/gates.py`
6. Wire Phase 7 (post-task telemetry) into `protocol/cycle.py`
7. Add `resources` MCP capability for lineage receipts
8. Implement `nexus_*` tool prefix routing in `engine/router.py`

### Medium-term (full premium loop)

9. Wire all 9 phases as an optional `ass-ade premium run` workflow
10. Add tier detection from key → available tool set
11. Implement LoRA flywheel integration (capture → contribute → reward)
12. Add SLA registration for enterprise contracts

### Long-term (enterprise)

13. VANGUARD continuous red-team as background service
14. Escrow-based outcome delivery for consulting/freelance use cases
15. A2A manifest advertising all 140 tools when premium key present
16. AEGIS epoch certification for EU AI Act compliance packaging

---

## 9. IP Boundary

Per the ASS-ADE public repo guardrails:

- **Public in this repo**: AAAA-Nexus endpoint names, prices, tier structure, workflow call order
- **Private / NOT in this repo**: sovereign invariant values, theorem counts, Codex constant derivations, UEP orchestrator engine internals
- **Delegated to AAAA-Nexus**: trust scoring math, compliance oracle implementation, hallucination detection model, routing heuristics

The premium workflow calls the endpoints and receives verdicts. It does not reimplement the backend.
