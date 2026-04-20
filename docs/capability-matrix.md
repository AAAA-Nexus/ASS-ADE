# Capability Matrix

## Legend

- ✅ Complete
- ⚠️ Partial
- ❌ Missing

## Core Product Surface

| Capability | Status | Notes |
| --- | ---: | --- |
| Public-safe Python CLI shell | ✅ | implemented and broad |
| Local config and profiles | ✅ | local, hybrid, premium |
| Local repo inspection | ✅ | doctor, repo summary, planning, protocol cycle |
| Local-first standalone value | ✅ | current core promise holds |
| Public/private guardrails | ✅ | documented and enforced in repo guidance |

## AAAA-Nexus Client Layer

| Capability | Status | Notes |
| --- | ---: | --- |
| Typed client for public endpoints | ✅ | broad surface implemented |
| Typed models and parsing | ✅ | production-grade |
| Structured errors | ✅ | implemented |
| Retry and circuit breaker | ✅ | implemented |
| Input validation | ✅ | validated at boundary |
| Policy preflight gate (`nexus_policy_preflight`) | ❌ | new hybrid capability |
| Trusted RAG augment (`nexus_trusted_rag_augment`) | ❌ | new hybrid capability |
| Synthesis guard (`nexus_synthesis_guard`) | ❌ | new hybrid capability |
| AHA detect (`nexus_aha_detect`) | ❌ | new premium capability |
| Autopoiesis plan (`nexus_autopoiesis_plan`) | ❌ | new premium capability |
| Trace certify (`nexus_trace_certify`) | ❌ | new premium capability |

## MCP

| Capability | Status | Notes |
| --- | ---: | --- |
| Remote MCP discovery | ✅ | supported |
| Remote MCP inspect and invoke | ✅ | supported |
| Dry-run invocation | ✅ | supported |
| Local mock MCP server | ✅ | supported |
| ASS-ADE MCP server | ✅ | current stdio roster on `2025-11-25`; prefer the live manifest over hard-coded counts |
| MCP manifest alignment | ✅ | current docs should reflect shipped state |

## A2A

| Capability | Status | Notes |
| --- | ---: | --- |
| Public A2A discovery | ✅ | supported |
| Validate agent card | ✅ | implemented |
| Negotiate capabilities | ✅ | implemented |
| Local card generation | ✅ | implemented |
| Capability matching and coordination flows | ⚠️ | primitives present; orchestration thin |

## Agent Shell

| Capability | Status | Notes |
| --- | ---: | --- |
| Multi-model provider layer | ✅ | implemented |
| Local tool execution | ✅ | implemented |
| Tool safety gating | ✅ | implemented |
| Diff preview and edit support | ✅ | implemented |
| Streaming loop output | ✅ | implemented |
| Interactive chat mode | ✅ | implemented |
| Single-shot run mode | ✅ | implemented |
| Token-aware conversation memory | ✅ | per-run only |
| Durable agent memory | ❌ | not implemented |
| Multi-agent coordination | ❌ | not implemented as a first-class loop |

## Workflows And Pipelines

| Capability | Status | Notes |
| --- | ---: | --- |
| trust-gate workflow | ✅ | implemented |
| certify workflow | ✅ | implemented |
| safe-execute workflow | ✅ | implemented |
| Sequential pipeline composition | ✅ | implemented |
| Progress callbacks | ✅ | implemented |
| Persistence and audit trail | ✅ | implemented for pipeline runs |
| Graph workflows | ⚠️ | richer orchestration still missing |
| Workflow templates | ⚠️ | limited |

## Distribution And UX

| Capability | Status | Notes |
| --- | ---: | --- |
| Python package | ✅ | current distribution mode |
| CI quality gate | ✅ | pytest, lint, type-check |
| VS Code extension | ❌ | not started |
| x402 payment UX | ❌ | not started |
| Cost estimation and consent UX | ❌ | not started |
