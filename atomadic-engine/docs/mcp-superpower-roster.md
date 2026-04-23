# AAAA-Nexus MCP Superpower Roster

This document captures the current hosted AAAA-Nexus MCP/API discovery pass and
turns it into an ASS-ADE superpower roster.

No admin key was used during this reconnaissance. All smoke tests used public
free endpoints or no-key trial calls, so the observed 2-4s latency on paid
trial endpoints is expected product behavior rather than a backend performance
regression.

## Hosted Discovery Facts

Public discovery surfaces checked:

- `https://atomadic.tech/.well-known/agent.json`
- `https://atomadic.tech/.well-known/mcp.json`
- `https://atomadic.tech/openapi.json`
- `https://atomadic.tech/.well-known/pricing.json`
- `https://atomadic.tech/health`
- `https://atomadic.tech/v1/metrics`

Current observed surface:

- hosted agent version: `0.5.1`
- A2A protocol version: `1.0.0`
- preferred transport: `JSONRPC`
- auth schemes: `Bearer`, `APIKey`, `x402`
- agent-card skills: `26`
- well-known MCP tools: `16`
- OpenAPI operations: `149`
- metrics endpoint reports: `119` endpoints across `30` product families
- pricing manifest: `14` free entries, `78` paid entries
- paid endpoint trial: `3` no-auth calls per endpoint per day, with an
  intentional free-tier delay to reduce IP-switching abuse and make paid
  priority latency visibly valuable

Important split:

- The direct `aaaa-nexus` MCP lane in `.mcp.json` launches the local
  `aaaa-nexus-mcp` server through `scripts/run_aaaa_nexus_mcp.py`, loads the
  workspace `.env` key, and calls the Cloudflare Worker-backed API at
  `https://atomadic.tech`.
- The `ass-ade` MCP lane in `.mcp.json` exposes local orchestration and wrapper
  tools.
- `/.well-known/mcp.json` is the hosted MCP superpower shortlist.
- `openapi.json` is the broader public REST contract.
- `/.well-known/pricing.json` exposes additional priced control-plane endpoints
  not currently listed in OpenAPI.
- The hosted `/mcp` JSON-RPC endpoint returned an initialize-style server
  envelope even for a `tools/list` probe, so the well-known MCP manifest is the
  practical source of truth for hosted MCP tools right now.

## Hosted MCP Shortlist

The hosted MCP manifest exposes these named tools:

| Tool | Endpoint | Price class |
| --- | --- | --- |
| `rng_quantum` | `GET /v1/rng/quantum` | free |
| `threat_score` | `POST /v1/threat/score` | paid |
| `hallucination_oracle` | `GET /v1/oracle/hallucination` | paid |
| `identity_verify` | `POST /v1/identity/verify` | paid |
| `ratchet_register` | `POST /v1/ratchet/register` | paid |
| `authorize_action` | `POST /v1/authorize/action` | paid |
| `spending_authorize` | `POST /v1/spending/authorize` | paid |
| `lineage_record` | `POST /v1/lineage/record` | paid |
| `contract_verify` | `POST /v1/contract/verify` | paid |
| `federation_mint` | `POST /v1/federation/mint` | paid |
| `aegis_mcp_proxy_execute` | `POST /v1/aegis/mcp-proxy/execute` | paid |
| `aegis_router_epistemic_bound` | `POST /v1/aegis/router/epistemic-bound` | paid |
| `vanguard_continuous_redteam` | `POST /v1/vanguard/continuous-redteam` | paid |
| `vanguard_mev_route_intent` | `POST /v1/vanguard/mev/route-intent` | paid |
| `vanguard_wallet_govern_session` | `POST /v1/vanguard/wallet/govern-session` | paid |
| `vanguard_escrow_lock_and_verify` | `POST /v1/vanguard/escrow/lock-and-verify` | paid |

## Live Smoke Findings

Representative no-key calls succeeded:

| Capability | Endpoint | Learned shape |
| --- | --- | --- |
| Health | `GET /health` | Returns build, epoch, HELIX integrity flags, provider, status. |
| RNG | `GET /v1/rng/quantum?count=1` | Returns `product`, `random`, `format`, `version`. |
| Metrics | `GET /v1/metrics` | Returns endpoint count, product family count, pricing summary. |
| Hallucination | `POST /v1/oracle/hallucination` | Body prefers `claim` and optional `context`; response includes KL threshold metadata. |
| Threat score | `POST /v1/threat/score` | Body requires `agent_id`; response includes behavior, intent, velocity scores. |
| Agent plan | `POST /v1/agents/plan` | Minimal `{goal}` works; complex `constraints` object failed schema validation. |
| Authorization | `POST /v1/authorize/action` | Requires `agent_id`, `action`, and `tool`; returns `authorization_token`. |
| AEGIS route | `POST /v1/aegis/router/epistemic-bound` | Returns decision, formal-bound metadata, and audit entry. |
| Quota create | `POST /v1/quota/tree` | Creates `tree_id`; child schema from local MCP is not fully honored by hosted endpoint. |
| Quota draw | `POST /v1/quota/tree/{id}/draw` | Requires `agent_id`, `tokens_requested`, optional `request_idempotency_key`. |
| Quota idempotency | repeated draw key | Returns `deduped: true`, `granted: 0`, and saved token count. |
| Memory fence | `POST /v1/memory/fence` | Returns `fence_id`, namespace key, purge behavior, and isolation level. |
| Consensus | `POST /v1/consensus/session` | Returns `session_id`, quorum threshold, expiry. |
| Consensus vote/result | vote then result | Result can return certificate even before quorum is met. |
| Output certifier | `POST /v1/certify/output` | Requires `agent_id` and `output_hash`; raw output is not the primary input. |

## Superpower Lanes

### Lane 1: Sovereign Safety

Purpose: block unsafe or low-confidence actions before local or remote execution.

Primary tools:

- `authorize_action`
- `threat_score`
- `aegis_mcp_proxy_execute`
- `aegis_router_epistemic_bound`
- `hallucination_oracle`
- `contract_verify`

ASS-ADE use:

- pre-tool execution gate
- pre-merge gate
- risky shell command gate
- premium synthesis guard

### Lane 2: Session And Identity Hardening

Purpose: make agent sessions, delegations, and identities survivable across
MCP/A2A environments.

Primary tools:

- `ratchet_register`
- RatchetGate status, advance, probe, verify
- identity verify/register/challenge
- delegation and UCAN endpoints
- `federation_mint`

ASS-ADE use:

- MCP session security
- cross-platform agent identity
- delegation-depth enforcement
- wallet/session approvals

### Lane 3: Coordination And Swarm

Purpose: turn primitives into real multi-agent workflows.

Primary tools:

- agent discovery/search/register/topology
- agent plan, intent, contradiction, semantic diff
- swarm relay/inbox/broadcast/topology
- consensus session, vote, result
- output certifier

ASS-ADE use:

- DADA orchestration
- multi-agent review
- independent verifier lane
- result notarization

### Lane 4: Quota, Budget, And Entitlement

Purpose: meter local and remote work with idempotent accounting.

Primary tools:

- quota tree, draw, status
- spending authorize and budget
- credits balance/history/usage
- payment fee and pricing manifests

ASS-ADE use:

- trial key limits
- free-to-paid conversion
- budget preview before remote calls
- admin-key QA harness with redacted logs

### Lane 5: Audit, Lineage, And Rollback

Purpose: make every meaningful action reviewable and reversible.

Primary tools:

- lineage record/trace
- audit log/trail/export
- rollback saga/checkpoint/compensate
- memory fence audit
- output certificate verification

ASS-ADE use:

- cycle reports
- release train audit
- postmortems
- workflow rollback planning

### Lane 6: Compliance And Trust

Purpose: convert agent actions into certificates users can understand.

Primary tools:

- compliance check, EU AI Act, fairness, explain, lineage
- drift check/certificate
- reputation record/score/history
- SLA register/report/status
- trust score/history/decay

ASS-ADE use:

- compliance-friendly release gate
- enterprise trust report
- support triage evidence
- SLA-backed paid workflows

### Lane 7: Inference And Knowledge

Purpose: give ASS-ADE real local-plus-remote intelligence without exposing the
private UEP brain.

Primary tools:

- trusted RAG augment
- inference and streaming inference
- embeddings/classification/models
- text summarize, extract, rewrite, keywords, similarity
- BitNet model catalog

ASS-ADE use:

- context refresh
- codebase summarization
- durable memory summaries
- cheap classification before expensive calls

### Lane 8: VANGUARD And High-Risk Finance

Purpose: keep finance and wallet actions inside the strongest safety envelope.

Primary tools:

- VANGUARD red team
- VANGUARD MEV route
- VANGUARD wallet governance
- VANGUARD escrow lock-and-verify
- DeFi risk, oracle, bridge, liquidation, contract audit

ASS-ADE use:

- never default free/local
- explicit user consent
- admin-only QA until payment UX is hardened
- premium demos and enterprise proof points

## Superpower Agent Roster

### 1. DADA Prime

Role: top-level orchestrator.

Owns:

- task classification
- lane selection
- work order generation
- separation between builder and verifier lanes

Backed by:

- `agents/plan`
- `authorize_action`
- consensus broker
- lineage record

### 2. AEGIS Sentinel

Role: MCP firewall and epistemic gate.

Owns:

- tool-call preflight
- prompt/tool injection scan path
- high-entropy or low-confidence blocking
- remote safety receipts

Backed by:

- `aegis_mcp_proxy_execute`
- `aegis_router_epistemic_bound`
- `threat_score`
- `hallucination_oracle`

### 3. Ratchet Warden

Role: session security governor.

Owns:

- session registration
- epoch advance
- session liveness
- MCP credential-theft mitigation posture

Backed by:

- RatchetGate register, status, advance, probe, verify

### 4. Quota Quartermaster

Role: entitlement, quota, and spend control.

Owns:

- quota tree creation
- idempotent token/call deduction
- free-tier cooldown enforcement
- threshold alerts

Backed by:

- quota tree/draw/status
- spending authorize
- credits usage
- pricing manifest

### 5. Ledger Scribe

Role: decision lineage and audit notary.

Owns:

- action trace capture
- audit trail export
- cycle report notarization
- release evidence

Backed by:

- lineage record/trace
- audit log/trail/export
- output certifier

### 6. Consensus Judge

Role: independent verifier and vote broker.

Owns:

- multi-agent review quorum
- confidence-weighted votes
- certified consensus result
- final release gate

Backed by:

- consensus session/vote/result
- output certificate verify
- agent contradiction
- semantic diff

### 7. Memory Fence Keeper

Role: safe durable memory boundary.

Owns:

- tenant/project isolation
- memory access audit
- purge-on-close workflows
- durable local memory bridge design

Backed by:

- memory fence create/audit
- trusted RAG augment
- local ASS-ADE memory store

### 8. Saga Marshal

Role: rollback coordinator.

Owns:

- multi-step workflow registration
- checkpoint tracking
- compensation action registry
- incident rollback execution

Backed by:

- rollback saga/checkpoint/compensate
- lineage
- audit

### 9. Trust Magistrate

Role: trust, reputation, and SLA gate.

Owns:

- trust and reputation lookup
- reputation event recording
- SLA checks
- Sybil and identity risk flags

Backed by:

- trust score/history/decay
- reputation score/history/record
- SLA status/report/register
- identity verify/sybil check

### 10. Compliance Marshal

Role: enterprise evidence builder.

Owns:

- compliance check bundles
- fairness/explainability/lineage certificates
- incident reports
- transparency reports

Backed by:

- compliance family
- drift certificate
- audit trail

### 11. Discovery Broker

Role: agent capability marketplace router.

Owns:

- finding external agents
- matching capabilities to tasks
- preparing handoffs
- routing to paid superpowers

Backed by:

- discovery search/recommend/registry
- agents search/discover/capabilities
- federation mint/verify/portability

### 12. VANGUARD Commander

Role: highest-risk financial and adversarial lane.

Owns:

- continuous red team
- MEV route protection
- governed wallet sessions
- escrow lock-and-verify

Backed by:

- VANGUARD family
- DeFi family
- escrow family

## First Trial Matrix

Use this matrix for admin-key QA. The harness must redact all key material and
avoid printing payment proofs. Call counts and bucket placement should remain
provisional until the full tool roster is complete and live enterprise testing
shows what each workflow actually costs.

| Priority | Endpoint/tool | Test goal | Expected pass signal |
| --- | --- | --- | --- |
| P0 | `authorize_action` | Can gate a local tool call. | `authorized: true` plus token. |
| P0 | quota tree/draw/status | Idempotent accounting works. | repeated key is `deduped`. |
| P0 | `aegis_router_epistemic_bound` | Safety route produces decision and audit. | decision plus audit entry hash. |
| P0 | `memory/fence` | Tenant boundary can be created. | `fence_id` and namespace key. |
| P0 | consensus session/vote/result | Verifier lane can notarize review. | `session_id`, vote count, certificate. |
| P1 | output certifier | Hash-based output certification works. | certificate hash; pass/fail rubric score. |
| P1 | lineage record/trace | Action trace can be retrieved. | record id then trace match. |
| P1 | RatchetGate lifecycle | Register, status, advance, verify. | epoch advances cleanly. |
| P1 | trusted RAG augment | Retrieval returns provenance payload. | chunk/source/receipt fields. |
| P1 | discovery/recommend | Tool/agent recommendation can power handoff. | ranked agents or capabilities. |
| P2 | VANGUARD redteam | Premium red-team demo. | findings and risk score. |
| P2 | contract verify | Behavioral contract attestation. | verdict and attestation id. |
| P2 | federation mint/verify | Cross-platform agent identity. | token then verified token. |

## ASS-ADE Product Roster

These are the agents ASS-ADE should expose as user-facing modes after the core
memory and coordination work lands:

1. **Build Captain**: plans and executes local repo changes with AEGIS preflight.
2. **Review Tribunal**: runs multi-agent review with consensus and output cert.
3. **Memory Steward**: writes and recalls durable task memory under memory fences.
4. **Quota Governor**: previews cost, checks quota, and manages upgrade prompts.
5. **Safety Sentinel**: gates risky shell/file/MCP calls through threat and auth.
6. **Compliance Packager**: turns a change into audit, compliance, and lineage artifacts.
7. **Release Marshal**: manages saga checkpoints, rollback plans, and canary evidence.
8. **Marketplace Scout**: discovers external agents and paid superpowers for a task.
9. **VANGUARD Operator**: handles high-risk finance and adversarial workflows.
10. **Support Triage Clerk**: maps user failures to quota, payment, auth, tool, or backend causes.

## Immediate Implementation Recommendation

Start with a hosted-superpower harness before building product UX:

1. Add a redacted admin-key smoke runner for the P0 trial matrix.
2. Generate typed endpoint notes from live responses, not only OpenAPI.
3. Capture per-tool latency, cost class, safety class, and workflow value.
4. Wire `authorize_action`, quota draw, AEGIS route, memory fence, and consensus into a single `superpower-preflight` prototype.
5. Use that prototype to design the final ASS-ADE coordination layer.
6. Derive free buckets only after enterprise-mode testing has enough signal.

The first killer workflow should be:

```text
task intent
  -> DADA Prime plan
  -> Quota Quartermaster budget preview
  -> AEGIS Sentinel safety gate
  -> Memory Fence Keeper session boundary
  -> Build Captain local action
  -> Consensus Judge independent review
  -> Ledger Scribe trace certificate
```
