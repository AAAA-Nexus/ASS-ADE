# Monetization And Access Control Plan

ASS-ADE should stay useful for free users while routing premium superpowers
through hosted AAAA-Nexus MCP/API endpoints.

The product line is:

```text
ASS-ADE public repo
  -> free local UEP-lite shell
  -> quota-aware hybrid client
  -> paid external MCP/API superpowers

AAAA-Nexus hosted platform
  -> metering, entitlement, x402, audit, trust, compliance, orchestration

Internal UEP
  -> private prompts, private theorem/proof machinery, private orchestration
```

## Product Shape

### Free ASS-ADE

Goal: prove value without requiring payment.

Includes:

- local repo inspection
- local planning
- local agent shell
- local MCP server
- basic public workflows
- a small number of hosted no-key or trial calls

Constraints:

- daily quotas
- intentional cooldown on free hosted superpower calls
- explicit upgrade paths when limits are reached

### Hybrid ASS-ADE

Goal: bridge free local workflows into live AAAA-Nexus contracts.

Includes:

- trial key
- bucketed quotas
- remote trust and security gates
- transparent remaining-call messaging
- no private UEP internals

### Premium ASS-ADE

Goal: paid superpowers with smoother latency, higher limits, and stronger
certification.

Includes:

- no free-tier delay
- higher caps
- priority backend handling where available
- call packs, subscriptions, or x402 pay-per-call

### Enterprise ASS-ADE

Goal: organization-grade control.

Includes:

- org keys
- pooled quotas
- audit exports
- allowlists
- custom endpoint bundles
- support and incident workflows

## Key Model

Every install should receive or attach an identity key on first remote connect.

Recommended key fields:

```json
{
  "key_id": "trial_...",
  "tier": "free|hybrid|premium|enterprise",
  "subject": "install|user|org",
  "scopes": ["bucket:A", "bucket:B", "bucket:C"],
  "issued_at": "2026-04-17T00:00:00Z",
  "expires_at": null,
  "quota_policy_id": "free-default-v1",
  "cooldown_policy_id": "free-cooldown-v1",
  "revoked": false
}
```

Rules:

- server-side entitlement is source of truth
- client counters are only hints
- keys can be rotated, revoked, and scoped
- admin QA keys must bypass billing while still logging usage
- admin key material is never printed, stored in reports, or sent to telemetry

## Buckets

Seed daily free defaults, for testing only:

| Bucket | Daily cap | Purpose | Examples |
| --- | ---: | --- | --- |
| A | 10 | frequent orchestration and status checks | authorization, quota status/draw, ratchet status, swarm relay, reputation score |
| B | 3 | premium proof or expensive gates | identity verify, contract verify, output certifier, VANGUARD, inference, compliance |
| C | 15 | lightweight productivity and reasoning | agent plan, intent classify, semantic diff, text tools, trusted RAG previews |

These caps are not final product limits. They are seed values for early ASS-ADE
testing while the full hosted tool roster is still being created. Final caps
should be set only after admin-key smoke tests measure per-tool cost, latency,
abuse risk, conversion pressure, and actual workflow value.

Bucket assignment should be server-owned and versioned. ASS-ADE can cache the
map for UX, but the backend decides final entitlement.

## Cap Calibration Loop

Exact call counts should be discovered from live product testing rather than
locked in during design.

Calibration inputs:

- full hosted MCP and REST endpoint roster
- per-tool runtime cost and backend saturation behavior
- average calls needed to complete useful free workflows
- conversion impact at 70%, 90%, and 100% thresholds
- observed abuse pressure from no-key and free-key traffic
- support burden from exhausted-quota and cooldown confusion
- paid-pack and subscription margin targets

Recommended loop:

1. Start with seed caps in the bucket table.
2. Run admin-key smoke tests against every completed endpoint.
3. Classify each endpoint into A/B/C or paid-only.
4. Measure useful workflow completion rate for free users.
5. Adjust caps weekly until free users can complete real work without giving
   away the premium lanes.
6. Promote the winning quota policy as a versioned server-side policy, such as
   `free-default-v2`.

## Cooldown Policy

The free/trial cooldown is intentional.

Purpose:

- reduce abuse from IP switching and scripted trial harvesting
- make paid/API-key latency visibly better
- preserve production-quality trial responses without giving away unlimited
  throughput

Recommended defaults:

| Tier | Added delay |
| --- | ---: |
| no-key trial | `2s` or current backend anti-abuse delay |
| free key | `2s` |
| hybrid paid pack | `0-0.5s` |
| premium subscription | `0s` |
| enterprise | `0s`, subject to contract SLO |

The client should present this as "free-tier cooldown" rather than "slow API."

## Entitlement Decision Contract

Before a hosted superpower call, ASS-ADE should be able to ask or infer:

```json
{
  "decision": "allow|warn|deny",
  "tier": "free",
  "bucket": "A",
  "endpoint": "/v1/authorize/action",
  "remaining_before": 4,
  "remaining_after_preview": 3,
  "reset_at": "2026-04-18T00:00:00Z",
  "cooldown_ms": 2000,
  "warnings": [],
  "upgrade_options": [
    {"type": "call_pack", "label": "Starter pack"},
    {"type": "monthly", "label": "Premium"},
    {"type": "x402", "label": "Pay per call"}
  ]
}
```

The final server response should still enforce the draw. Client preflight is UX,
not authority.

## Quota Draw Contract

Every billable or quota-counted call should include an idempotency key.

```json
{
  "key_id": "trial_...",
  "endpoint": "/v1/quota/tree/{id}/draw",
  "bucket": "A",
  "units_requested": 1,
  "request_idempotency_key": "uuid-or-trace-id"
}
```

Expected properties:

- repeated idempotency keys must not double-charge
- quota draw and endpoint execution should share a trace id
- threshold alerts fire at 70%, 90%, and 100%
- exhaustion returns an upgrade payload, not a vague error

## Exhaustion Response

```json
{
  "error": "quota_exhausted",
  "tier": "free",
  "bucket": "B",
  "used": 3,
  "limit": 3,
  "reset_at": "2026-04-18T00:00:00Z",
  "cooldown_ms": 2000,
  "message": "You used today's 3 premium proof calls.",
  "upgrade_options": [
    {
      "type": "call_pack",
      "label": "Buy 500 calls",
      "url": "https://atomadic.tech/pay"
    },
    {
      "type": "x402",
      "label": "Pay once for this call"
    }
  ]
}
```

## Billing Paths

### Call Packs

Best for occasional users.

Rules:

- pack balance burns after free quota
- pack balance should not expire by default
- pack usage is visible in ASS-ADE status output

### Monthly Subscription

Best for regular users.

Rules:

- subscription caps override free caps
- subscription gets reduced or zero cooldown
- pack balance remains available for overage or burst usage

### x402 Pay-Per-Call

Best for agents and burst usage.

Rules:

- always show amount and recipient before proof generation
- enforce amount ceilings client-side too
- validate treasury recipient before signing
- record payment proof redacted in local audit

## Conversion UX

### Before Call

Show:

- bucket
- remaining calls
- cooldown
- whether this call is paid, trial, or free

### At 70%

Soft nudge:

- "You have 3 of 10 safety-gate calls left today."
- suggest one useful upgrade path

### At 90%

Strong nudge:

- show plan comparison
- show one-click purchase link

### At 100%

Hard stop:

- preserve local fallback when possible
- show reset time
- show call-pack, monthly, and x402 options

### After High-Value Success

Post-success upsell:

- "This certified review used one premium proof call. Upgrade to run this across
  the whole repo."

## Server-Side Guardrails

Required:

- per-key rate limits
- per-IP rate limits
- per-endpoint and per-bucket caps
- soft device binding for key-sharing signals
- replay protection through idempotency keys
- key rotation and revocation
- suspicious burst detection
- quota draw logs
- conversion funnel events
- fraud signal events

## Admin QA Mode

Admin QA keys should allow trial-and-error across paid endpoints without payment
friction.

Rules:

- use the same public client path as paid users
- send key via normal API-key headers
- redact key and payment material in all output
- log endpoint, status, product id, latency, and schema notes
- never commit admin keys or generated payment proofs
- never write raw response bodies containing secrets

Recommended local environment variable:

```text
AAAA_NEXUS_API_KEY=<redacted>
```

## Implementation Slices

### Slice 0: Contracts And Docs

- bucket map
- entitlement decision schema
- exhaustion response schema
- QA key policy
- superpower roster

### Slice 1: Client UX

- show remaining calls before known remote calls
- parse 402 and quota exhaustion responses
- add explicit paid-call confirmation
- render reset time and upgrade links

### Slice 2: Redacted Smoke Harness

- admin-key support
- endpoint matrix runner
- schema capture
- latency capture
- no secret logging

### Slice 3: Gateway Workflow

Create a `superpower-preflight` workflow:

```text
intent
  -> quota preview
  -> authorize action
  -> AEGIS epistemic route
  -> memory fence
  -> local execution
  -> consensus review
  -> lineage record
```

### Slice 4: Product Rollout

- free bundle
- trial alerts
- exhaustion UX
- call packs
- monthly subscriptions
- x402 fallback

### Slice 5: Enterprise Controls

- org keys
- pooled quotas
- audit exports
- endpoint allowlists
- SLO dashboard

## Ninety-Day Rollout

| Phase | Window | Goal |
| --- | --- | --- |
| Phase 1 | weeks 1-2 | Draft bucket map, key schema, quota APIs, exhaustion payloads. |
| Phase 2 | weeks 3-5 | Implement server metering, alerts, cooldown, and upgrade UX. |
| Phase 3 | weeks 6-8 | Add call packs, monthly subscriptions, and x402 fallback. |
| Phase 4 | weeks 9-12 | Finalize quotas from telemetry and add enterprise controls. |

## Immediate Defaults

- Free seed caps for testing: `A=10`, `B=3`, `C=15` daily.
- Cooldown: `2s` on no-key/free/trial calls only.
- Alerts: `70%`, `90%`, `100%`.
- Paid: no cooldown where possible, higher caps, priority path.
- Purchase: call packs for occasional users, subscription for regular users,
  x402 for burst usage.

The seed caps remain provisional until the hosted tool roster is complete and
the admin-key QA matrix has enough data to set product limits with confidence.
