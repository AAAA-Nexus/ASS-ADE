# Roadmap

See immediate execution priorities in `docs/next-moves.md`.

## Track A - Repo Guardrails: Complete

Shipped:

- public/private boundary rules
- contributor guardrails
- stack guidance for a sanitized public shell

## Track B - Public Shell: Complete

Shipped:

- local CLI foundation
- config and profile handling
- repo summary and planning helpers
- useful local-only workflows

## Track C - Hybrid AAAA-Nexus Integration: Complete

Shipped:

- typed AAAA-Nexus client layer
- public contract discovery for OpenAPI, A2A, and MCP
- remote workflow and verification commands
- hybrid profile support without leaking backend internals

## Track D - Production Hardening: Complete

Shipped:

- resilient transports and typed exceptions
- CLI input validation at the network boundary
- hero workflows
- session lifecycle management
- CI gates and stable test coverage growth

## Track E - Agentic Shell, MCP, And Pipeline Layer: Complete

Shipped:

- multi-model engine and provider routing
- built-in tools with undo support
- token-aware conversation trimming and token budgeting
- agent loop with streaming events and quality gates
- MCP server support
- A2A validation, discovery, negotiation, and local card generation
- workflow pipeline engine with progress callbacks and persistence
- atomic multi-file edit planning

## Track F - Durable Memory, Coordination, And Editor UX: Next

This is now the real next track. The earlier roadmap items around basic A2A and
MCP support are already shipped.

### Priority 1: Durable Agent Memory

Outcome:

The agent can retain useful task state beyond one process lifetime without
leaking private backend internals.

Scope:

- durable local memory store for task summaries and working state
- memory write and recall hooks for the agent loop
- optional pruning and summarization paths
- clear boundary between local memory and premium remote memory services

### Priority 2: Agent Coordination Layer

Outcome:

ASS-ADE can coordinate multiple agents using the primitives that already exist
in the client surface.

Scope:

- coordination manager over discovery, relay, inbox, and consensus endpoints
- handoff state and shared task context
- workflow patterns for agent delegation and result collection
- coordination-safe audit trail and persistence

### Priority 3: x402 Payment UX

Outcome:

Billable calls are explicit, reviewable, and auditable from the public client.

Scope:

- HTTP 402 metadata parsing
- cost estimation before execution
- explicit user consent for billable calls
- local billing log and budget controls

### Priority 4: Editor-Native Integration

Outcome:

The existing MCP and agent surfaces become easy to use from VS Code.

Scope:

- VS Code extension scaffold
- MCP auto-registration and onboarding
- workflow and memory history views
- cost and status surfaces in-editor

### Priority 5: Expanded Coordination Workflows

Outcome:

The repo ships higher-level workflows built on memory and coordination, not just
single-agent hero paths.

Candidates:

- `audit-full`
- `onboard-agent`
- `deploy-guard`
- multi-agent review and certification flows

## Ongoing Constraint

Never let the public repo become a mirror of the private backend. Prefer typed
contracts, thin clients, and public-safe UX over backend disclosure.
