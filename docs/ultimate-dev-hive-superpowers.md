# Ultimate Dev Hive Superpower List

This is the enterprise-first ASS-ADE roster. The goal is to build the full
superpower system first, test it with an admin key, then derive the free,
hybrid, premium, and enterprise bundles from measured cost and workflow value.

No free-call counts are final in this document. Bucket placement comes after
tool completion and live testing.

## Product Rule

Build in this order:

1. Enterprise full power mode.
2. Admin-key QA harness with redacted logs.
3. Workflow cost and value measurement.
4. Paid product bundles.
5. Free bucket strip-down.

This keeps ASS-ADE honest: free users get useful workflows, paid users get
visible superpowers, and internal UEP logic stays private.

## Connection Layer

| Superpower | Status | Purpose |
| --- | --- | --- |
| Nexus MCP Connector | wired | Connect ASS-ADE to hosted AAAA-Nexus MCP/API with API key, bearer, and x402 paths. |
| Redacted Admin QA Harness | partial | Exercise paid tools freely with admin key while never logging secrets or payment proofs. |
| Endpoint Schema Miner | to build | Learn request and response shapes from live calls, OpenAPI, pricing, and MCP manifests. |
| Tool Registry Sync | manifest wired | Keep local ASS-ADE aware of hosted MCP tools, REST endpoints, prices, cooldowns, and capability tags. |
| Phase 0 Recon Gate | wired | Enforces Never Code Blind with repo recon plus latest technical-document source targets. |
| Context Packet Builder | wired | Packages source URLs and hashed repo excerpts before planning or code generation. |
| Local Vector Memory | wired local | Stores and queries trusted local context through a generic vector-memory layer. |
| MAP = TERRAIN Gate | wired | Halt execution when a required agent, hook, skill, tool, harness, prompt, or instruction is missing and produce a rebuild-backed invention packet. |
| Entitlement Preview | to build | Show whether a call is free, paid, trial, admin, exhausted, or cooldown-gated. |
| Product Bundle Compiler | to build | Convert tested tools into free, paid, enterprise, and internal-only bundles. |

Current connection status:

- `.env` key loading is active through `AAAA_NEXUS_API_KEY`.
- `.mcp.json` now exposes two MCP lanes:
  `aaaa-nexus` for the direct Cloudflare Worker-backed AAAA-Nexus MCP server,
  and `ass-ade` for the local ASS-ADE orchestration server.
- The direct `aaaa-nexus` lane uses `scripts/run_aaaa_nexus_mcp.py` to load the
  workspace `.env` key without storing secrets in `.mcp.json`.
- The direct worker lane sets `AAAA_NEXUS_BASE_URL=https://atomadic.tech`,
  `AAAA_NEXUS_TIMEOUT=5.0`, and `AAAA_NEXUS_AUTOGUARD=false` for fast admin QA.
- Remote MCP manifest discovery is working.
- Paid MCP invocation is working with token/proof redaction enabled by default.
- Direct worker probe passes with the key redacted in output. Observed warm
  calls: `/v1/payments/fee` at ~50ms and `/.well-known/mcp.json` at ~48ms from
  the current workstation.
- `phase0_recon` is implemented as a local MCP/CLI gate for Never Code Blind.
- `context_pack`, `context_memory_store`, and `context_memory_query` are
  implemented as local MCP tools and CLI commands.
- `MAP = TERRAIN` is implemented as local ASS-ADE MCP tool `map_terrain` and
  direct AAAA-Nexus MCP shim `nexus_map_terrain`.

## Enterprise Spine

These are the mandatory superpowers for the full enterprise version.

| Superpower | Backing tools | Purpose |
| --- | --- | --- |
| DADA Prime Orchestrator | local orchestrator, agent plan, MCP registry | Converts user intent into work orders, lanes, gates, and verifier tasks. |
| AEGIS Safety Gate | `authorize_action`, `threat_score`, AEGIS router, hallucination oracle | Blocks risky actions before shell, file, MCP, payment, or deployment calls. |
| Ratchet Warden | RatchetGate, identity, federation | Secures sessions, delegation, epoch movement, and agent identity. |
| Quota Quartermaster | quota tree/draw/status, spending authorize, pricing | Performs budget previews, idempotent deductions, and entitlement decisions. |
| Memory Fence Keeper | memory fence, audit, rollback | Creates isolated memory boundaries for users, repos, agents, and tasks. |
| Ledger Scribe | lineage, audit trail, output certifier | Records who did what, why, with which tools, and which proof/certificate was produced. |
| Consensus Judge | consensus session/vote/result, verifier agents | Separates builder and reviewer lanes and creates quorum-backed review evidence. |
| Saga Marshal | rollback saga, checkpoints, compensating actions | Makes risky workflows reversible and release-safe. |
| Compliance Marshal | compliance, drift, fairness, explainability | Produces enterprise-readable trust, compliance, and release packets. |
| VANGUARD Commander | VANGUARD redteam, wallet governance, MEV, escrow | Handles high-risk finance, adversarial workflows, and premium red-team tasks. |

## Dev Hive Capabilities

These are the user-visible developer superpowers.

| Superpower | Status | Purpose |
| --- | --- | --- |
| Codebase Cartographer | to build | Builds repo maps, dependency graphs, ownership maps, and change impact views. |
| Intent-to-Plan Engine | hosted plus local | Turns ambiguous requests into scoped implementation plans and acceptance criteria. |
| Work Order Splitter | to build | Splits work into builder, reviewer, tester, docs, and release lanes. |
| MCP Tool Smith | to build | Creates new local MCP tools from repeated workflows and validates schemas. |
| API Contract Smith | to build | Generates typed clients, schemas, and smoke tests from OpenAPI and live responses. |
| Capability Synthesizer | wired foundation | Applies MAP = TERRAIN, emits repo-native assets, and creates certified qk/at/mo/og/sy invention packets for missing capabilities. |
| Auto Linter | to build | Runs formatting, static analysis, secrets checks, doc-boundary lint, prompt-boundary lint, and MCP schema lint. |
| Security Sentinel | hosted plus local | Runs threat scoring, dependency checks, secret scans, and permission checks. |
| Test Harness Captain | local | Creates unit, integration, e2e, regression, and chaos test packs. |
| Golden Fixture Builder | to build | Captures stable request/response fixtures for endpoint and workflow regression tests. |
| Build Doctor | local | Diagnoses failing installs, dependency conflicts, flaky tests, and broken scripts. |
| Release Marshal | hosted plus local | Creates canary plans, rollback evidence, post-release checks, and changelog packets. |
| Docs Boundary Guard | local | Keeps public ASS-ADE docs separated from internal UEP-only material. |
| Support Triage Clerk | to build | Converts user failures into quota, auth, billing, schema, network, or product issues. |

## Trust RAG And LoRA Stack

This is the learning spine for the Dev Hive and the highest-leverage product
surface in the whole system. The enterprise goal is a Cloudflare-backed shared
RAG/LoRA loop where many developer agents contribute only verified, trusted,
privacy-scrubbed improvements into a common adapter mesh.

| Superpower | Status | Purpose |
| --- | --- | --- |
| Phase 0 Recon Agent | wired local | Finds relevant repo files and blocks technical work until source URLs are attached. |
| Trust-Based RAG | local foundation | Retrieves only trusted, scored, provenance-bearing context for code, docs, audits, and decisions. |
| Provenance Ranker | partial | Scores context by source presence, file hash, and repo-local relevance; hosted trust scoring still pending. |
| RAG Citation Packet | wired local | Produces compact source packets for prompts, reviews, and LoRA training examples. |
| Local Vector Memory | wired local | Deterministic local vector store for trusted context and task lessons. |
| Experience Trace Capture | to build | Records task, plan, tool calls, diffs, tests, approvals, failures, and final outcome. |
| Training Example Curator | to build | Converts high-trust traces into clean instruction/input/output examples. |
| Privacy Scrubber | to build | Removes secrets, private paths, paid keys, customer data, and internal-only UEP text. |
| Shared LoRA Foundry | to build | Trains shared adapters from trusted traces and curated RAG packets. |
| LoRA Registry | local plus hosted | Stores adapter metadata, base model checksum, dataset hash, eval score, and rollout state. |
| Adapter Eval Gate | to build | Blocks LoRA promotion unless it improves target workflows without regression. |
| Adapter Rollback | to build | Reverts bad adapters and records why the promotion failed. |
| Skill Distiller | to build | Converts repeated success patterns into reusable ASS-ADE skills and tool policies. |

Primary flywheel:

```text
phase0_recon
  -> context_pack
  -> trust-gated RAG packet
  -> verified execution
  -> fix/sample capture
  -> privacy scrub
  -> shared LoRA training queue
  -> eval-gated adapter promotion
  -> better agents and better future samples
```

Cloudflare target substrate:

- Workers for the RAG and LoRA control plane
- D1 for registry, contribution metadata, eval scores, and rewards
- Vectorize for semantic memory
- R2 for trusted corpora and training artifacts
- Durable Objects for contribution dedupe, batch coordination, and ledgers
- Queues for scrub, eval, train, promote, and rollback jobs

## Automation And Quality Superpowers

| Superpower | Status | Purpose |
| --- | --- | --- |
| Multi-Linter Mesh | to build | Coordinates language linters, type checkers, formatters, security scanners, and custom ASS policy checks. |
| Prompt Linter | to build | Detects leaked internal prompts, private UEP internals, unsupported claims, and unsafe tool instructions. |
| MCP Contract Linter | to build | Validates tool names, schemas, auth requirements, error envelopes, and idempotency behavior. |
| Pricing Linter | to build | Checks pricing manifests for missing tiers, invalid units, unsafe x402 defaults, and inconsistent free trials. |
| Quota Policy Linter | to build | Checks bucket definitions, cooldown text, reset rules, and upgrade payloads. |
| UX Copy Linter | to build | Ensures paywall and cooldown messaging is clear, honest, and not hostile. |
| Audit Artifact Linter | to build | Ensures reports contain enough evidence without leaking secrets. |
| Release Gate Linter | to build | Blocks releases missing smoke tests, rollback plan, docs, or changelog. |

## Swarm And Collaboration Superpowers

| Superpower | Status | Purpose |
| --- | --- | --- |
| Agent Roster Compiler | to build | Builds task-specific teams from available local agents and hosted superpowers. |
| Verifier Lane | hosted plus local | Keeps independent review separate from implementation. |
| Debate And Consensus | hosted plus local | Uses consensus sessions for high-impact design and code decisions. |
| Swarm Inbox | hosted | Routes tasks, updates, and review requests across agents. |
| Agent Reputation | hosted | Tracks which agents and tools are reliable for each task class. |
| Capability Marketplace Scout | hosted plus local | Finds external agents, endpoints, and paid capabilities for a workflow. |
| Human Approval Bridge | to build | Pauses for human approval on irreversible, costly, or high-risk actions. |

## Monetization And Product Superpowers

These are enabled after enterprise-mode testing produces enough data.

| Superpower | Status | Purpose |
| --- | --- | --- |
| Free Bucket Designer | later | Chooses which tools belong in A/B/C after cost and workflow testing. |
| Conversion Journey Agent | later | Adds 70%, 90%, and 100% trial nudges based on measured user value. |
| Plan Compiler | later | Builds Starter, Pro, Team, Enterprise, and x402 pay-per-call bundles. |
| Call Pack Ledger | later | Tracks purchased packs, burn order, expiration policy, and receipts. |
| Subscription Entitlements | later | Applies monthly caps, priority queue, and pooled org quotas. |
| Fraud Sentinel | later | Detects IP switching, scripted trial harvesting, key sharing, and replay abuse. |
| Meter Transparency Reporter | later | Shows users what was called, why it cost what it cost, and what remains. |

## Initial Enterprise Workflow

The first full-power workflow should prove the whole system:

```text
user intent
  -> DADA Prime Orchestrator
  -> Phase 0 Recon Gate
  -> Context Packet Builder
  -> Local Vector Memory recall
  -> Endpoint Schema Miner
  -> Quota Quartermaster preview
  -> AEGIS Safety Gate
  -> Memory Fence Keeper
  -> Codebase Cartographer
  -> Trust-Based RAG packet
  -> Build Captain implementation
  -> Auto Linter
  -> Test Harness Captain
  -> Consensus Judge
  -> Output Certifier
  -> Ledger Scribe
  -> Experience Trace Capture
  -> Training Example Curator
  -> Shared LoRA Foundry queue
```

## Testing Metrics Before Free Buckets

For each tool and workflow, capture:

- auth mode used
- request schema notes
- response schema notes
- latency with admin key
- latency without key, if allowed
- cost class
- safety class
- failure modes
- retry behavior
- idempotency behavior
- secrets exposure risk
- workflow value score
- support-risk score
- proposed product tier

## Build Priority

1. Finish the Redacted Admin QA Harness.
2. Endpoint Schema Miner.
3. Enterprise Spine workflow.
4. Hosted Trust-Based RAG upgrade.
5. Experience Trace Capture.
6. Auto Linter.
7. Shared LoRA Foundry.
8. Product Bundle Compiler.
9. Free Bucket Designer.
