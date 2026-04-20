# Architecture

## Core Model

ASS-ADE is a public shell around private backend systems.

The repo is allowed to expose:

- local developer utility
- typed public-contract clients
- public-safe orchestration surfaces
- degraded local fallbacks
- certificates, reports, and attestations returned by public endpoints

The repo is not allowed to expose:

- private backend internals
- unpublished verification corpora
- private scoring, routing, or monetization heuristics
- backend orchestration logic that would weaken the moat

That boundary is the product.

## System Shape

```text
User
  -> ASS-ADE CLI / MCP server / local agent shell
    -> local tools, local planning, local pipelines
    -> public MCP and A2A contracts
    -> typed AAAA-Nexus client
      -> private Atomadic backend systems
```

## Current Open Surface

The current public repo contains:

- Typer-based CLI with 30 sub-apps
- local repo summary and public-safe protocol cycle commands
- multi-model provider layer for OpenAI-compatible backends and AAAA-Nexus inference
- agent loop with token-aware conversation management and streaming events
- tool registry with 8 built-in tools
- undo history and atomic multi-file edit planning
- A2A validation and negotiation helpers
- remote MCP client helpers plus a local MCP server and mock server
- workflow and pipeline layers for trust, certification, and safe execution

## Current Closed Surface

The differentiated logic remains behind remote contracts:

- premium orchestration and coordination behavior
- stronger backend trust, policy, and attestation logic
- payment, routing, and internal scoring controls
- private evaluation harnesses and unpublished reasoning systems

## Product Tiers

### Tier 1: Local Utility

Shipped today.

Examples:

- file operations and shell execution
- repo summary and protocol cycle reporting
- local planning helpers
- agent loop with local or OpenAI-compatible providers
- MCP mock server and local tool execution

### Tier 2: Hybrid Utility

Shipped today.

Examples:

- typed AAAA-Nexus client usage
- trust, identity, and hallucination checks
- hero workflows and pipeline commands
- A2A validation and negotiation
- RatchetGate session lifecycle
- MCP tool discovery and invocation helpers

### Tier 3: Premium Black Box

Still intentionally remote.

Examples:

- premium expert services
- stronger control-plane coordination
- backend-only attestation and policy logic
- billable premium routing and monetization flows

## Current Agent Architecture

The current agent stack has four layers:

1. provider selection
2. conversation management
3. tool execution
4. optional remote quality gates

### Provider Selection

`engine/router.py` resolves providers in this order:

1. explicit OpenAI-compatible provider override
2. OpenAI credentials
3. Anthropic-compatible routing path
4. AAAA-Nexus inference for hybrid and premium profiles
5. Ollama fallback

### Conversation Management

`agent/conversation.py` maintains per-run message state with token-aware trimming.

What exists now:

- preserved system prompt
- token budget tracking per model context window
- eviction of oldest non-system messages when needed

What does not exist yet:

- durable cross-session agent memory
- task summaries or recall store for later runs
- shared memory across cooperating agents

### Tool Execution

`agent/loop.py` supports plan/act/observe repetition with a 25-round tool limit and streaming events.

What exists now:

- built-in file and shell tools
- optional quality-gated tool execution
- token-aware request budgeting
- epistemic routing hints for complexity-aware model selection

What does not exist yet:

- multi-agent task delegation inside the loop
- consensus, relay, or inbox integration as first-class loop behavior
- coordinator state for handoff, retries, and shared progress

## Memory Surfaces

There are three distinct memory-like surfaces in the current codebase.

### 1. Conversation Memory

In-memory only.

- stored in `Conversation`
- trimmed to token budget
- discarded when the process ends

### 2. Edit Memory

Persistent local undo history.

- stored under `.ass-ade/history/`
- records file snapshots before writes and edits
- supports `undo_edit`

### 3. Workflow Memory

Persistent pipeline execution results.

- stored when `Pipeline` is configured with a persistence directory
- useful for replay, audit, and reporting
- not yet integrated into the agent loop as durable task memory

## Coordination Surfaces

The coordination primitives exist mostly as typed clients and commands today.

Available now:

- A2A validation and negotiation
- discovery search, recommend, and registry commands
- swarm, consensus, quota, and related client methods in `NexusClient`
- MCP server exposure for hero workflows, A2A helpers, and agent access

Missing now:

- a first-class coordination engine that uses these primitives together
- agent handoff and shared task state
- durable memory attached to coordination flows
- multi-agent workflow templates built on discovery, relay, and consensus

## Resilience Architecture

The client stack supports composable transports:

```text
httpx.HTTPTransport
  -> RetryTransport
  -> CircuitBreakerTransport
```

Typed exceptions map HTTP failures into actionable client errors, and CLI-facing validation runs before network calls.

## Workflow Architecture

There are two workflow layers.

### Hero Workflows

Direct multi-step functions in `workflows.py`:

- `trust_gate`
- `certify_output`
- `safe_execute`

### Pipeline Layer

Composable pipeline execution in `pipeline.py`:

- sequential steps with shared context
- fail-fast or continue-on-failure behavior
- progress callbacks
- result persistence to disk

This means the repo already has workflow persistence and progress hooks, but it still lacks async graph execution and higher-level composed workflow libraries.

## Decision Rule For New Features

Before adding a feature, ask:

1. Does it create real local or hybrid value?
2. Does it leak private strategic logic?
3. Is the right public shape a local helper, typed client, contract adapter, or attestation consumer?
4. Should durable memory or coordination live locally, remotely, or as a mixed design?

If publishing the exact implementation would weaken the moat, it belongs behind AAAA-Nexus.
