# Public Protocol

This document defines the public-safe improvement cycle for ASS-ADE.

ASS-ADE may borrow public-safe process patterns from private systems, but it must not embed private instruction bodies, private orchestration logic, unpublished verification material, or hidden monetization behavior.

## Allowed Inheritance

The public repo may inherit:

- structured assess/design/audit/reflect loops
- typed public-contract integration
- local-first defaults with explicit remote opt-in
- iterative improvement over public code and public contracts

The public repo must not inherit:

- private instruction bodies
- unpublished proof machinery
- backend orchestration internals
- hidden routing or pricing heuristics

## ASS-ADE Public Enhancement Cycle

### 1. Assess

- inspect repo shape and toolchain status
- inspect current local, hybrid, or premium profile assumptions
- inspect tests, docs, and public contracts
- identify whether claims in docs still match code

### 2. Design

- choose the smallest useful public-safe improvement
- prefer local utility, typed clients, or contract adapters
- keep premium or moat-sensitive behavior behind AAAA-Nexus

### 3. Audit

- confirm docs and guardrails remain accurate
- confirm local mode remains safe and useful
- confirm remote behavior is contract-driven
- confirm no private internals leaked into the repo

### 4. Reflect

- summarize what changed
- record the next highest-value public-safe improvement
- decide whether the next gap belongs locally, remotely, or as a mixed design

## Current Audit Focus

As of the current codebase, the most important audit questions are:

1. Are docs aligned with the actual CLI, MCP, A2A, and workflow surfaces?
2. Does the agent loop still have only per-run conversation memory?
3. Are coordination primitives present only as clients and commands, or do they exist as real orchestration flows?
4. Are billable remote calls still explicit and user-controlled?

## CLI Support

Run the full cycle:

```bash
ass-ade cycle "Improve the public shell"
```

Run the protocol report directly:

```bash
ass-ade protocol run "Improve the public shell"
```

Write markdown or JSON artifacts:

```bash
ass-ade cycle "Improve the public shell" --report-out .ass-ade/reports/latest-cycle.md
ass-ade cycle "Improve the public shell" --json-out .ass-ade/reports/latest-cycle.json
```

Record evolution events:

```bash
ass-ade protocol evolution-record birth \
  --summary "Initial public birth and maiden self-rebuild" \
  --command "ass-ade doctor" \
  --command "python -m pytest tests/ -q --no-header" \
  --report RECON_REPORT.md \
  --report ECO_SCAN_REPORT.md
```

Generate the split-branch evolution demo:

```bash
ass-ade protocol evolution-demo \
  --branches tests-first,docs-first,safety-first \
  --iterations 3 \
  --write
```

Update version surfaces after a winning branch is merged:

```bash
ass-ade protocol version-bump patch --summary "Release the selected evolution path"
```

The evolution ledger writes `.ass-ade/evolution/ledger.jsonl`,
per-event JSON snapshots under `.ass-ade/evolution/events/`, and the
human-readable `EVOLUTION.md`. It records decision summaries, command receipts,
metrics, reports, artifacts, and lineage IDs. It does not record secrets or
private chain-of-thought.

## Current Audit Criteria

### Core Criteria

1. Local mode remains the default and is still useful.
2. Public behavior remains contract-driven.
3. Documentation matches the current codebase.
4. Premium value stays behind AAAA-Nexus boundaries.

### Current Release Criteria

1. Resilience layer is present.
2. Input validation exists at the CLI boundary.
3. Hero workflows and pipeline commands are operational.
4. MCP server and A2A surfaces are documented accurately.
5. Agent memory and coordination limitations are stated plainly.

## Design Intent

This protocol exists to improve ASS-ADE without teaching the world how the private backend works.
