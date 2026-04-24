# Capability Matrix

> Generated: 2026-04-20T08:21:11Z  |  source: `capabilities/registry.json`

## Summary

| Status | Count |
| --- | ---: |
| OK | 26 |
| PARTIAL | 3 |
| MISSING | 5 |

## Legend

- `OK`: implemented and covered by local evidence.
- `PARTIAL`: usable, but with known product or integration gaps.
- `MISSING`: known gap.

## Gaps (action required)

- `a2a.task_lifecycle` — A2A task lifecycle and coordination state [MISSING]
- `agent.coordination` — First-class multi-agent coordination loop [MISSING]
- `agent.durable_memory` — Durable cross-session agent memory [MISSING]
- `ide.vscode_extension` — VS Code extension and editor-native UX [MISSING]
- `payment.cost_consent_budget` — Cost estimation, consent, and budget UX [MISSING]
- `mcp.local_server` — ASS-ADE local MCP server [PARTIAL]
- `payment.x402_low_level` — Low-level x402 challenge and proof handling [PARTIAL]
- `workflow.pipeline_graph` — Graph workflows and reusable coordination templates [PARTIAL]

## A2A

| ID | Capability | Status | Evidence | Notes |
| --- | --- | :---: | --- | --- |
| `a2a.task_lifecycle` | A2A task lifecycle and coordination state | MISSING | [`docs/implementation-status.md`](docs/implementation-status.md), [`docs/gap-report.md`](docs/gap-report.md) |  |
| `a2a.validate_discover_negotiate` | A2A validate, discover, negotiate, and local-card | OK | [`src/ass_ade/a2a/__init__.py`](src/ass_ade/a2a/__init__.py), [`src/ass_ade/commands/a2a.py`](src/ass_ade/commands/a2a.py), [`tests/test_a2a.py`](tests/test_a2a.py) (+1 more) |  |

## Agent

| ID | Capability | Status | Evidence | Notes |
| --- | --- | :---: | --- | --- |
| `agent.coordination` | First-class multi-agent coordination loop | MISSING | [`docs/e2e-workflow-gaps.md`](docs/e2e-workflow-gaps.md), [`docs/roadmap.md`](docs/roadmap.md) |  |
| `agent.durable_memory` | Durable cross-session agent memory | MISSING | [`docs/gap-report.md`](docs/gap-report.md), [`docs/next-moves.md`](docs/next-moves.md) |  |
| `agent.shell` | Agent shell with tools, streaming events, and quality gates | OK | [`src/ass_ade/agent/loop.py`](src/ass_ade/agent/loop.py), [`src/ass_ade/tools/builtin.py`](src/ass_ade/tools/builtin.py), [`tests/test_agent.py`](tests/test_agent.py) (+1 more) |  |
| `agent.token_memory` | Token-aware per-run conversation memory | OK | [`src/ass_ade/agent/conversation.py`](src/ass_ade/agent/conversation.py), [`tests/test_agent.py`](tests/test_agent.py), [`tests/test_tokens.py`](tests/test_tokens.py) |  |

## Blueprint

| ID | Capability | Status | Evidence | Notes |
| --- | --- | :---: | --- | --- |
| `blueprint.design` | Blueprint design from prompt or context | OK | [`src/ass_ade/engine/rebuild/feature.py`](src/ass_ade/engine/rebuild/feature.py), [`src/ass_ade/commands/feature.py`](src/ass_ade/commands/feature.py), [`tests/test_feature_proposer.py`](tests/test_feature_proposer.py) |  |
| `blueprint.validate` | Blueprint registry and validation | OK | [`src/ass_ade/commands/blueprint.py`](src/ass_ade/commands/blueprint.py), [`tests/test_blueprint_command.py`](tests/test_blueprint_command.py) |  |

## Certification

| ID | Capability | Status | Evidence | Notes |
| --- | --- | :---: | --- | --- |
| `certification.local` | Local codebase certification | OK | [`src/ass_ade/local/certifier.py`](src/ass_ade/local/certifier.py), [`tests/test_certifier.py`](tests/test_certifier.py) |  |

## Context

| ID | Capability | Status | Evidence | Notes |
| --- | --- | :---: | --- | --- |
| `context.pack_vector_memory` | Context packets and local vector memory primitives | OK | [`src/ass_ade/context_memory.py`](src/ass_ade/context_memory.py), [`tests/test_recon_context.py`](tests/test_recon_context.py) | Primitive context memory exists; durable agent memory is tracked separately. |

## Core

| ID | Capability | Status | Evidence | Notes |
| --- | --- | :---: | --- | --- |
| `core.config_profiles` | Local, hybrid, and premium config profiles | OK | [`src/ass_ade/config.py`](src/ass_ade/config.py), [`tests/test_config.py`](tests/test_config.py) |  |
| `core.public_cli` | Public-safe Python CLI shell | OK | [`src/ass_ade/cli.py`](src/ass_ade/cli.py), [`tests/test_cli.py`](tests/test_cli.py), [`tests/test_cli_happy_path.py`](tests/test_cli_happy_path.py) | Broad Typer command surface with local-first defaults. |
| `core.public_private_guardrails` | Public/private boundary guardrails | OK | [`AGENTS.md`](AGENTS.md), [`CONTRIBUTING.md`](CONTRIBUTING.md), [`docs/dev-stack.md`](docs/dev-stack.md) |  |
| `core.repo_inspection` | Local repository inspection | OK | [`src/ass_ade/local/repo.py`](src/ass_ade/local/repo.py), [`tests/test_repo_summary.py`](tests/test_repo_summary.py) |  |

## Docs

| ID | Capability | Status | Evidence | Notes |
| --- | --- | :---: | --- | --- |
| `docs.engine` | Local docs generation and repository documentation synthesis | OK | [`src/ass_ade/local/docs_engine.py`](src/ass_ade/local/docs_engine.py), [`tests/test_docs_engine.py`](tests/test_docs_engine.py) |  |

## Evolution

| ID | Capability | Status | Evidence | Notes |
| --- | --- | :---: | --- | --- |
| `evolution.split_merge_stress_gate` | Split-evolution, merge-sibling, and feature-gain stress gate | OK | [`scripts/ass_ade_local_control.py`](scripts/ass_ade_local_control.py), [`docs/local-control.md`](docs/local-control.md), [`docs/stress-test-evolution-gain.md`](docs/stress-test-evolution-gain.md) (+1 more) | Added to prove evolutions gain measurable features before promotion. |

## IDE

| ID | Capability | Status | Evidence | Notes |
| --- | --- | :---: | --- | --- |
| `ide.vscode_extension` | VS Code extension and editor-native UX | MISSING | [`docs/roadmap.md`](docs/roadmap.md), [`docs/next-moves.md`](docs/next-moves.md) |  |

## MCP

| ID | Capability | Status | Evidence | Notes |
| --- | --- | :---: | --- | --- |
| `mcp.local_server` | ASS-ADE local MCP server | PARTIAL | [`src/ass_ade/mcp/server.py`](src/ass_ade/mcp/server.py), [`tests/test_mcp_server_streaming.py`](tests/test_mcp_server_streaming.py) | Works locally; editor-grade threading and VS Code polish remain open. |
| `mcp.remote_discovery` | Remote MCP discovery, inspect, dry-run, and invocation | OK | [`src/ass_ade/cli.py`](src/ass_ade/cli.py), [`tests/test_mcp.py`](tests/test_mcp.py), [`tests/test_mcp_extended.py`](tests/test_mcp_extended.py) |  |

## Nexus

| ID | Capability | Status | Evidence | Notes |
| --- | --- | :---: | --- | --- |
| `nexus.resilience` | Retry, timeout, and circuit-breaker transports | OK | [`src/ass_ade/nexus/resilience.py`](src/ass_ade/nexus/resilience.py), [`tests/test_resilience.py`](tests/test_resilience.py) |  |
| `nexus.typed_client` | Typed AAAA-Nexus public client layer | OK | [`src/ass_ade/nexus/client.py`](src/ass_ade/nexus/client.py), [`src/ass_ade/nexus/models.py`](src/ass_ade/nexus/models.py), [`tests/test_nexus_client_comprehensive.py`](tests/test_nexus_client_comprehensive.py) |  |
| `nexus.validation` | Boundary input validation and SSRF protections | OK | [`src/ass_ade/nexus/validation.py`](src/ass_ade/nexus/validation.py), [`tests/test_validation.py`](tests/test_validation.py), [`tests/test_ssrf_protection.py`](tests/test_ssrf_protection.py) |  |

## Payment

| ID | Capability | Status | Evidence | Notes |
| --- | --- | :---: | --- | --- |
| `payment.cost_consent_budget` | Cost estimation, consent, and budget UX | MISSING | [`docs/capability-matrix.md`](docs/capability-matrix.md), [`docs/next-moves.md`](docs/next-moves.md) |  |
| `payment.x402_low_level` | Low-level x402 challenge and proof handling | PARTIAL | [`src/ass_ade/nexus/x402.py`](src/ass_ade/nexus/x402.py), [`tests/test_x402_flow.py`](tests/test_x402_flow.py), [`tests/test_search_x402.py`](tests/test_search_x402.py) |  |

## Provider

| ID | Capability | Status | Evidence | Notes |
| --- | --- | :---: | --- | --- |
| `provider.multi_model` | Multi-provider model routing | OK | [`src/ass_ade/engine/provider.py`](src/ass_ade/engine/provider.py), [`src/ass_ade/commands/providers.py`](src/ass_ade/commands/providers.py), [`tests/test_free_providers.py`](tests/test_free_providers.py) |  |

## Quality

| ID | Capability | Status | Evidence | Notes |
| --- | --- | :---: | --- | --- |
| `quality.enhance_scan` | Local enhancement scanner | OK | [`src/ass_ade/local/enhancer.py`](src/ass_ade/local/enhancer.py), [`tests/test_enhancer.py`](tests/test_enhancer.py) |  |
| `quality.linter` | Monadic linter facade | OK | [`src/ass_ade/local/linter.py`](src/ass_ade/local/linter.py), [`tests/test_linter.py`](tests/test_linter.py) |  |

## Rebuild

| ID | Capability | Status | Evidence | Notes |
| --- | --- | :---: | --- | --- |
| `rebuild.engine` | Five-tier rebuild engine | OK | [`src/ass_ade/engine/rebuild/orchestrator.py`](src/ass_ade/engine/rebuild/orchestrator.py), [`tests/test_engine.py`](tests/test_engine.py), [`tests/test_phase1_integration.py`](tests/test_phase1_integration.py) |  |
| `rebuild.output_governance` | Dedicated local rebuild output metadata and validation | OK | [`schemas/ass_ade_output.schema.json`](schemas/ass_ade_output.schema.json), [`scripts/ass_ade_local_control.py`](scripts/ass_ade_local_control.py), [`tests/test_local_control.py`](tests/test_local_control.py) | Added for local split-evolution and merge-sibling maintenance. |
| `rebuild.tier_purity` | Monadic tier purity checks | OK | [`src/ass_ade/engine/rebuild/tier_purity.py`](src/ass_ade/engine/rebuild/tier_purity.py), [`tests/test_monadic_purity.py`](tests/test_monadic_purity.py) |  |
| `rebuild.version_tracking` | Per-artifact and aggregate version tracking | OK | [`src/ass_ade/engine/rebuild/version_tracker.py`](src/ass_ade/engine/rebuild/version_tracker.py), [`tests/test_version_tracker.py`](tests/test_version_tracker.py) |  |

## Workflow

| ID | Capability | Status | Evidence | Notes |
| --- | --- | :---: | --- | --- |
| `workflow.pipeline_graph` | Graph workflows and reusable coordination templates | PARTIAL | [`docs/capability-matrix.md`](docs/capability-matrix.md), [`docs/roadmap.md`](docs/roadmap.md) |  |
| `workflow.hero_trust_certify_safe` | Trust-gate, certify, and safe-execute hero workflows | OK | [`src/ass_ade/workflows.py`](src/ass_ade/workflows.py), [`tests/test_workflows.py`](tests/test_workflows.py) |  |
| `workflow.pipeline_sequential` | Sequential pipeline engine with persistence | OK | [`src/ass_ade/pipeline.py`](src/ass_ade/pipeline.py), [`tests/test_pipeline.py`](tests/test_pipeline.py) |  |
