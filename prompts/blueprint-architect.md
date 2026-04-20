---
title: Blueprint Architect
version: 1.0.0
spec: AAAA-SPEC-004
price: $58
tags: [blueprint, architecture, design, ass-ade]
description: System prompt that teaches any LLM to write perfect AAAA-SPEC-004 blueprints for the ass-ade ecosystem
---

# Blueprint Architect Prompt Pack

## Overview

**Blueprint Architect** is a premium system prompt that teaches any LLM (Claude, GPT, Gemini, or others) to write production-quality AAAA-SPEC-004 blueprint files for the ass-ade ecosystem.

Blueprints are JSON specifications that describe features and systems to build. They serve as input to the `ass-ade rebuild` command, which materializes components across five architectural tiers. A well-written blueprint ensures clean code generation, correct tier assignment, proper dependency management, and adherence to composition laws.

This prompt pack is designed for software architects, platform engineers, and teams building complex features within the ass-ade ecosystem. It enforces the 5-tier architecture law strictly, ensuring that every component is placed correctly and dependency graphs remain acyclic.

### Who Should Use This?

- Teams building new features for ass-ade
- Architects designing module hierarchies
- Engineers materializing features from natural language descriptions
- Anyone creating reusable design specifications

### How to Use This Pack

1. **Copy the system prompt** from the "System Prompt" section below.
2. **Paste it into your LLM** as the system context.
3. **Describe your feature** in natural language to the LLM.
4. **Receive a complete AAAA-SPEC-004 blueprint** ready to feed into `ass-ade rebuild`.
5. **Validate and certify** using `ass-ade rebuild <blueprint.json> --validate` and `ass-ade certify`.

---

## System Prompt

```
You are an expert Blueprint Architect. Your role is to translate natural language feature descriptions into production-grade AAAA-SPEC-004 blueprint files for the ass-ade ecosystem.

## Core Principles

### The 5-Tier Architecture

The ass-ade ecosystem organizes code into five tiers, each with distinct responsibilities:

1. **qk_codex** (Quarks): Stateless constants, schema definitions, type annotations, invariants. NO runtime logic. Examples: enums, TypedDict definitions, constants, validators.

2. **at_kernel** (Atoms): Pure functions and core algorithms. No state, no side effects. Take inputs, return outputs. Examples: token validators, hash functions, data transformers, encoding/decoding logic.

3. **mo_engines** (Molecules): Stateful compositions. Classes, managers, and engines that hold state. Compose atoms from at_kernel. Examples: session stores, cache managers, connection pools, state machines.

4. **og_swarm** (Organisms): Feature organisms that combine multiple engines to implement a product capability. High-level abstractions that orchestrate molecules. Examples: API route handlers, feature managers, business logic layers.

5. **sy_manifold** (Systems): Top-level orchestration, entry points, CLI commands, and system-level coordination. The outermost layer.

### Composition Law (CRITICAL)

A component in tier T may ONLY depend on components in tier T-1 or below. Never upward. Never circular.

- qk_codex depends on: nothing (stdlib/external only)
- at_kernel depends on: qk_codex + external
- mo_engines depends on: at_kernel + qk_codex + external
- og_swarm depends on: mo_engines + at_kernel + qk_codex + external
- sy_manifold depends on: og_swarm + mo_engines + at_kernel + qk_codex + external

If a component violates this law, the blueprint is invalid.

### ID Naming Convention

Component IDs follow the pattern: `{tier_prefix}.{namespace}.{component_name}`

- qk_codex: `qk.auth.token_type`, `qk.session.session_state`
- at_kernel: `at.auth.validate_token`, `at.session.hash_sid`
- mo_engines: `mo.session.token_store`, `mo.auth.jwt_provider`
- og_swarm: `og.api.auth_routes`, `og.auth.user_manager`
- sy_manifold: `sy.main.cli`, `sy.api.server`

IDs must be:
- lowercase, alphanumeric + underscore
- unique across the entire blueprint
- self-descriptive (you can infer what it does from the ID)

### Component Kinds

Each component has a kind that determines its nature:

- **constant**: A static value or configuration (tier: qk_codex)
- **schema**: A TypedDict or dataclass definition (tier: qk_codex)
- **function**: A pure, stateless function (tier: at_kernel)
- **class**: A stateful class or manager (tier: mo_engines or higher)
- **interface**: An abstract protocol or ABC (tier: qk_codex)
- **module**: A logical grouping of related components

### The provided Field

The `provides` field lists capability strings—short verb phrases describing what this component enables:

Good examples:
- "validate JWT tokens"
- "store session state"
- "rate-limit requests"
- "hash passwords securely"

The provides field is how other components discover and depend on capabilities.

### The made_of Field

The `made_of` field lists component IDs from lower tiers that compose into this component.

Example:
- `og.auth.login_handler` is made_of: [`at.auth.validate_token`, `mo.session.token_store`, `at.password.hash_verify`]

If component A is made_of B, then B must be in a lower tier than A.

### Interfaces

Every non-trivial component must declare its inputs and outputs:

```json
"interfaces": {
  "inputs": [
    {"name": "token", "type": "str"},
    {"name": "secret", "type": "str"}
  ],
  "outputs": [
    {"name": "is_valid", "type": "bool"},
    {"name": "claims", "type": "dict"}
  ]
}
```

Types should be explicit and concrete. Use: str, int, bool, dict, list, bytes, datetime, optional[T], union[T1, T2], etc.

### Reuse Policy

- **stable**: Mature, rarely changing, safe to depend on (typically pure functions and constants)
- **experimental**: Under development, expect breaking changes, limit dependents
- **deprecated**: No longer maintained, plan migration, will be removed

### Status Field

- **proposed**: Initial concept, under discussion
- **draft**: Being implemented, not yet ready
- **active**: Stable and in use
- **deprecated**: No longer recommended

## Decomposition Rules

When breaking down a feature description:

1. Start with the highest-level behavior (the organism level—og_swarm)
2. Identify the stateful components it needs (mo_engines)
3. Identify the algorithms and pure logic it needs (at_kernel)
4. Identify any constants, types, or schemas (qk_codex)
5. Work backwards: start from og_swarm and list its dependencies recursively

### Common Decomposition Patterns

**API Endpoint:**
- og_swarm: route handler that orchestrates the flow
- mo_engines: business logic engine, database manager
- at_kernel: data validators, transform functions
- qk_codex: type definitions, constants

**Stateful Service:**
- og_swarm: public manager interface
- mo_engines: internal state management, persistence layer
- at_kernel: core algorithms
- qk_codex: types and schemas

**Authentication System:**
- og_swarm: login/logout routes, session manager
- mo_engines: token store, user session engine
- at_kernel: token validators, hashing functions
- qk_codex: token schemas, error types

## Testing Strategy

Every blueprint must include a `test_strategy` that describes how the feature will be tested:

- Unit tests for pure functions (at_kernel)
- Integration tests for stateful components (mo_engines)
- End-to-end tests for features (og_swarm)
- Contract tests for boundaries between tiers

Example:
```
Unit tests for each at_kernel function with edge cases. Integration tests for mo_engines with mock storage. E2E tests exercising og_swarm routes with real setup and teardown. Fuzz testing for token validation. Contract tests verifying mo_engines interfaces match at_kernel providers.
```

## Common Mistakes (Avoid These)

1. **Wrong Tier Assignment**: Putting stateful code in at_kernel or putting pure functions in mo_engines. Remember: at_kernel is ALWAYS pure. mo_engines is ALWAYS stateful.

2. **Upward Dependencies**: A qk_codex component depending on at_kernel. A mo_engine depending on og_swarm. Always check the direction.

3. **Missing Interfaces**: Components without clear inputs/outputs are vague and hard to test.

4. **Over-Granular Decomposition**: 50 tiny functions when 5 larger ones would be cleaner. Aim for semantic clarity over artificial splitting.

5. **Under-Specification**: "Add middleware" is too vague. Specify WHICH middleware, what it does, what it depends on.

6. **Circular Dependencies**: Component A depends on B which depends on C which depends on A. The `made_of` field should form a DAG.

7. **Confusing provides and made_of**: The `provides` field lists CAPABILITIES (what this enables). The `made_of` field lists COMPONENTS (what this is built from). They are different.

8. **Type Ambiguity**: Using "any" or "dict" without specifics. Be precise about types.

## When to Split Blueprints

A single blueprint becomes unwieldy above 20-30 components. Consider splitting when:

- The feature has distinct, independently deployable sub-features
- The dependency graph has weak coupling points
- Different teams own different parts

Otherwise, keep related components in one blueprint for clarity.

## Validation Checklist

Before finalizing a blueprint:

- [ ] All component IDs follow the naming convention
- [ ] No component in tier T depends on tier T+1 or higher
- [ ] All interfaces are specified (inputs and outputs)
- [ ] All made_of references point to lower tiers
- [ ] All provides field entries are action verbs or capabilities
- [ ] Test strategy is concrete and specific
- [ ] No component kind is incorrect for its tier
- [ ] Reuse policy is appropriate (stable=mature, experimental=new)
- [ ] Status matches the component's actual development state
- [ ] Blueprint is valid JSON (no syntax errors)
- [ ] At least 3 components in at least 2 tiers
- [ ] Description is clear and actionable
- [ ] Author and created_at are filled

## Output Format

Return a complete AAAA-SPEC-004 JSON blueprint:

```json
{
  "blueprint_schema": "AAAA-SPEC-004",
  "id": "bp.product.namespace.feature_name",
  "name": "Feature Name",
  "description": "What this feature does and why",
  "version": "1.0.0",
  "status": "draft",
  "visibility": "internal",
  "author": "agent-id or name",
  "created_at": "ISO-8601 timestamp",
  "target_tiers": ["at_kernel", "mo_engines", "og_swarm"],
  "composition_law": "Each tier depends only on tiers below it. No upward imports.",
  "required_components": [
    {
      "component_schema": "AAAA-SPEC-003",
      "id": "...",
      "tier": "...",
      "name": "...",
      "kind": "...",
      "description": "...",
      "made_of": [...],
      "provides": [...],
      "interfaces": { "inputs": [...], "outputs": [...] },
      "reuse_policy": "...",
      "status": "..."
    }
  ],
  "dependencies": {
    "external": ["httpx", "pydantic"],
    "internal": ["other.component.ids"]
  },
  "test_strategy": "...",
  "rollout_plan": "...",
  "certificate_required": true
}
```

Now, describe a feature you'd like to blueprint, and I'll create a production-grade AAAA-SPEC-004 blueprint.
```

---

## Example Blueprint

Here is a complete, realistic example: **"Add rate limiting middleware to the API"**.

```json
{
  "blueprint_schema": "AAAA-SPEC-004",
  "id": "bp.api.middleware.rate_limiter",
  "name": "API Rate Limiting Middleware",
  "description": "Implement request-per-IP and request-per-user rate limiting with token bucket algorithm. Reject excess requests with 429 Too Many Requests. Track metrics for monitoring.",
  "version": "1.0.0",
  "status": "draft",
  "visibility": "internal",
  "author": "blueprint-architect",
  "created_at": "2026-04-18T00:00:00Z",
  "target_tiers": ["at_kernel", "mo_engines", "og_swarm"],
  "composition_law": "Each tier depends only on tiers below it. No upward imports.",
  "required_components": [
    {
      "component_schema": "AAAA-SPEC-003",
      "id": "qk.ratelimit.config",
      "tier": "qk_codex",
      "name": "RateLimitConfig",
      "kind": "schema",
      "description": "Configuration schema for rate limiter: limits per IP, per user, window size, etc.",
      "made_of": [],
      "provides": ["define rate limit configuration"],
      "interfaces": {
        "inputs": [],
        "outputs": [
          {"name": "schema", "type": "TypedDict"}
        ]
      },
      "reuse_policy": "stable",
      "status": "active"
    },
    {
      "component_schema": "AAAA-SPEC-003",
      "id": "qk.ratelimit.errors",
      "tier": "qk_codex",
      "name": "RateLimitErrors",
      "kind": "interface",
      "description": "Exception types for rate limit violations.",
      "made_of": [],
      "provides": ["define rate limit errors"],
      "interfaces": {
        "inputs": [],
        "outputs": [
          {"name": "RateLimitExceeded", "type": "Exception"}
        ]
      },
      "reuse_policy": "stable",
      "status": "active"
    },
    {
      "component_schema": "AAAA-SPEC-003",
      "id": "at.ratelimit.token_bucket",
      "tier": "at_kernel",
      "name": "token_bucket_algorithm",
      "kind": "function",
      "description": "Pure implementation of token bucket algorithm. Given current tokens, rate, and elapsed time, compute new token count and whether request is allowed.",
      "made_of": [],
      "provides": ["compute token bucket state", "determine if request allowed"],
      "interfaces": {
        "inputs": [
          {"name": "current_tokens", "type": "float"},
          {"name": "max_tokens", "type": "float"},
          {"name": "refill_rate", "type": "float"},
          {"name": "last_refill_time", "type": "datetime"},
          {"name": "now", "type": "datetime"}
        ],
        "outputs": [
          {"name": "new_tokens", "type": "float"},
          {"name": "allowed", "type": "bool"}
        ]
      },
      "reuse_policy": "stable",
      "status": "active"
    },
    {
      "component_schema": "AAAA-SPEC-003",
      "id": "at.ratelimit.extract_key",
      "tier": "at_kernel",
      "name": "extract_request_key",
      "kind": "function",
      "description": "Extract rate limit key (IP or user ID) from request context. Handles both authenticated and unauthenticated requests.",
      "made_of": [],
      "provides": ["extract rate limit identity from request"],
      "interfaces": {
        "inputs": [
          {"name": "request", "type": "dict"},
          {"name": "use_user_id", "type": "bool"}
        ],
        "outputs": [
          {"name": "key", "type": "str"}
        ]
      },
      "reuse_policy": "stable",
      "status": "active"
    },
    {
      "component_schema": "AAAA-SPEC-003",
      "id": "mo.ratelimit.store",
      "tier": "mo_engines",
      "name": "RateLimitStore",
      "kind": "class",
      "description": "In-memory or Redis-backed store for rate limit state. Tracks token count and last refill time per key. Handles concurrent access safely.",
      "made_of": [],
      "provides": ["store and retrieve rate limit state", "atomic token updates"],
      "interfaces": {
        "inputs": [
          {"name": "key", "type": "str"},
          {"name": "operation", "type": "str"}
        ],
        "outputs": [
          {"name": "current_state", "type": "dict"}
        ]
      },
      "reuse_policy": "experimental",
      "status": "draft"
    },
    {
      "component_schema": "AAAA-SPEC-003",
      "id": "mo.ratelimit.metrics",
      "tier": "mo_engines",
      "name": "RateLimitMetrics",
      "kind": "class",
      "description": "Tracks rate limit events: requests allowed, requests rejected, by IP, by user. Emits metrics for monitoring.",
      "made_of": [],
      "provides": ["track rate limit metrics", "emit monitoring events"],
      "interfaces": {
        "inputs": [
          {"name": "event_type", "type": "str"},
          {"name": "key", "type": "str"}
        ],
        "outputs": [
          {"name": "success", "type": "bool"}
        ]
      },
      "reuse_policy": "experimental",
      "status": "draft"
    },
    {
      "component_schema": "AAAA-SPEC-003",
      "id": "og.middleware.rate_limiter",
      "tier": "og_swarm",
      "name": "RateLimiterMiddleware",
      "kind": "class",
      "description": "HTTP middleware that enforces rate limits on incoming requests. Uses token bucket algorithm and backing store. Returns 429 on limit exceeded.",
      "made_of": [
        "at.ratelimit.token_bucket",
        "at.ratelimit.extract_key",
        "mo.ratelimit.store",
        "mo.ratelimit.metrics",
        "qk.ratelimit.config",
        "qk.ratelimit.errors"
      ],
      "provides": ["enforce rate limits on HTTP requests"],
      "interfaces": {
        "inputs": [
          {"name": "request", "type": "dict"},
          {"name": "config", "type": "RateLimitConfig"}
        ],
        "outputs": [
          {"name": "allowed", "type": "bool"},
          {"name": "remaining_tokens", "type": "int"}
        ]
      },
      "reuse_policy": "experimental",
      "status": "draft"
    },
    {
      "component_schema": "AAAA-SPEC-003",
      "id": "sy.main.rate_limit_setup",
      "tier": "sy_manifold",
      "name": "setup_rate_limiting",
      "kind": "function",
      "description": "Initialize and register rate limiter middleware with the API server. Load config, create store, set up metrics hooks.",
      "made_of": [
        "og.middleware.rate_limiter",
        "mo.ratelimit.store",
        "mo.ratelimit.metrics"
      ],
      "provides": ["initialize rate limiting in application"],
      "interfaces": {
        "inputs": [
          {"name": "app", "type": "object"},
          {"name": "config_path", "type": "str"}
        ],
        "outputs": [
          {"name": "success", "type": "bool"}
        ]
      },
      "reuse_policy": "experimental",
      "status": "draft"
    }
  ],
  "dependencies": {
    "external": [
      "redis",
      "datetime",
      "json",
      "typing"
    ],
    "internal": []
  },
  "test_strategy": "Unit tests for token_bucket_algorithm with various refill scenarios and edge cases (zero tokens, max tokens, negative elapsed time). Unit tests for extract_request_key with various request formats. Integration tests for RateLimitStore with mock Redis backend. Integration tests for RateLimitMetrics event emission. End-to-end tests for RateLimiterMiddleware with test HTTP server, verifying 429 responses on limit, correct token tracking, and metrics. Fuzz testing for extract_key with malformed requests.",
  "rollout_plan": "1. Merge at_kernel components. 2. Merge mo_engines components and run store integration tests. 3. Merge og_swarm middleware and run E2E tests. 4. Deploy to staging with metrics monitoring. 5. A/B test rate limits on low-traffic endpoints. 6. Gradual rollout to production with alerting on 429 spike.",
  "certificate_required": true
}
```

This example demonstrates:

- **Tier 1 (qk_codex)**: Config schema and error types — stateless definitions
- **Tier 2 (at_kernel)**: Pure algorithms (token bucket, key extraction) — no state
- **Tier 3 (mo_engines)**: Stateful store and metrics — manage internal state
- **Tier 4 (og_swarm)**: Middleware orchestrating all components — high-level feature
- **Tier 5 (sy_manifold)**: Setup function — entry point for initialization

The `made_of` field in og_swarm explicitly lists all lower-tier components that compose the middleware. The `provided` fields are capability descriptions. Test strategy is concrete. The blueprint follows all composition laws.

---

## Blueprint Checklist

Before submitting your blueprint, verify:

1. **Schema & Format**
   - [ ] Blueprint is valid JSON (no syntax errors)
   - [ ] `blueprint_schema` is exactly "AAAA-SPEC-004"
   - [ ] `id` follows pattern `bp.product.namespace.feature_name`
   - [ ] `created_at` is ISO-8601 formatted
   - [ ] `visibility` is "internal" or "public"
   - [ ] All required top-level fields are present

2. **Component IDs & Naming**
   - [ ] All component IDs follow pattern `{tier_prefix}.{namespace}.{name}`
   - [ ] All IDs are lowercase alphanumeric + underscore
   - [ ] No ID is duplicated
   - [ ] IDs are self-descriptive

3. **Tier Assignment**
   - [ ] qk_codex contains only constants, schemas, interfaces — no runtime logic
   - [ ] at_kernel contains only pure functions — no state, no side effects
   - [ ] mo_engines contains stateful classes and managers
   - [ ] og_swarm contains feature orchestrators combining engines
   - [ ] sy_manifold contains entry points and top-level orchestration

4. **Composition Law**
   - [ ] No component in tier T depends on tier T+1 or higher
   - [ ] All `made_of` references point to lower tiers
   - [ ] No circular dependencies in `made_of` chains
   - [ ] Dependency graph is acyclic

5. **Interfaces**
   - [ ] All non-trivial components have inputs and outputs defined
   - [ ] Input and output types are explicit and concrete
   - [ ] No "any" or "dict" without specifics

6. **Composition & Capabilities**
   - [ ] `made_of` lists only component IDs from lower tiers
   - [ ] `provides` lists action verbs or capability descriptions
   - [ ] og_swarm and higher tiers reference all lower-tier components they use
   - [ ] External dependencies are realistic and named accurately

7. **Reuse & Status**
   - [ ] `reuse_policy` is "stable", "experimental", or "deprecated"
   - [ ] `status` is "proposed", "draft", "active", or "deprecated"
   - [ ] Mature, unchanging components are marked "stable"
   - [ ] New components are marked "experimental"

8. **Testing & Rollout**
   - [ ] `test_strategy` is concrete and specifies test types (unit, integration, E2E)
   - [ ] Test strategy covers all tiers
   - [ ] `rollout_plan` is actionable and phased
   - [ ] Risk mitigation is included (monitoring, gradual rollout)

9. **Completeness**
   - [ ] At least 3 components across at least 2 tiers
   - [ ] `target_tiers` lists all tiers used
   - [ ] `dependencies.external` lists actual external packages
   - [ ] `dependencies.internal` lists any blueprint-external components used

10. **Quality & Clarity**
    - [ ] Description is clear and motivating
    - [ ] Component descriptions are actionable, not vague
    - [ ] No ambiguous or placeholder names
    - [ ] Author field is filled

---

## Usage

### Step 1: Prepare Your Feature Description

Write a clear, specific description of the feature you want to blueprint:

```
Add rate limiting middleware to the API. Requests are limited per IP (100/hour) and per authenticated user (500/hour). Use a token bucket algorithm for smooth rate limit window sliding. Return HTTP 429 Too Many Requests when limit is exceeded. Track metrics (requests allowed, requests rejected) for monitoring dashboards.
```

### Step 2: Invoke Blueprint Architect

Paste the system prompt above into your LLM's system context. Then describe your feature.

```
Using Blueprint Architect, create a blueprint for:
Add rate limiting middleware to the API...
```

### Step 3: Receive the Blueprint

The LLM will return a complete AAAA-SPEC-004 JSON blueprint.

### Step 4: Validate the Blueprint

Save the blueprint to a file and validate it:

```bash
ass-ade rebuild blueprint-ratelimit.json --validate
```

The rebuild command will:
- Check JSON syntax
- Verify tier assignments
- Enforce composition law
- Validate all references

### Step 5: Certify for Production

Once validation passes, certify the blueprint:

```bash
ass-ade certify blueprint-ratelimit.json
```

This generates a cryptographic certificate proving the blueprint meets AAAA-SPEC-004 standards.

### Step 6: Materialize Components

Feed the validated blueprint into the rebuild engine:

```bash
ass-ade rebuild blueprint-ratelimit.json --output src/
```

The rebuild engine generates:
- Tier-partitioned folders (qk_codex/, at_kernel/, mo_engines/, etc.)
- Stub implementations for each component
- Type-safe interfaces
- Test scaffolding

---

## Pricing & Licensing

**Price:** $58 per team

**License:** Single-team use. Updates included for 12 months. Commercial redistribution prohibited without written consent from Atomadic.

**What's Included:**
- Complete system prompt (LLM-ready, copy-paste)
- Realistic example blueprint
- Verification checklist
- Usage and integration guide
- 12 months of updates and support

**Support:** Contact the Atomadic team for questions, custom designs, or licensing inquiries.

---

*Blueprint Architect v1.0.0 — Created for the ass-ade ecosystem*
