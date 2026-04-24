# ASS-ADE Launch Day Shopping List
_Generated: 2026-04-24 — sourced from `C:\!atomadic` ecosystem scan_

This is the cherry-pick shopping list for assimilating high-value features from the `!atomadic`
ecosystem into the current monadic ASS-ADE-SEED spine.

---

## PRIORITY 1 — Multilang Rebuild Engine (`ass-ade-v1/engine/rebuild/`)
**Source:** `C:/!atomadic/ass-ade-v1/src/ass_ade/engine/rebuild/`

| File | Symbols | Why |
|------|---------|-----|
| `gap_filler.py` | `build_gap_fill_plan`, `propose_components`, `assess_blueprint_fulfillment`, `ProposedComponent` | The "gap fill" the user asked about — fills missing monadic building blocks automatically |
| `bridge_emitter.py` | `emit_multilang_bridge_suite` | Emits Rust/TS/Kotlin/Swift bridge packages from native stubs |
| `bridge_manifest.py` | `bridge_dir`, `bridge_manifest_path`, `load_bridge_manifest` | Tracks which languages have bridge packages |
| `synthesis.py` | `synthesize_missing_components`, `consume_last_nexus_error`, `SynthesisFailure` | Calls Nexus to write missing functions |
| `epiphany_cycle.py` | `build_epiphany_document`, `detect_track_and_steps`, `hypotheses_from_epiphanies` | Drives the AI-assisted breakthrough cycle |
| `tier_purity.py` | `check_tier_purity`, `enforce_tier_purity`, `tier_prefix_from_id` | Validates monadic import law on emitted trees |
| `import_rewriter.py` | `rewrite_imports`, `build_stem_map` | Rewrites cross-tier imports to be compliant |
| `conflict_detector.py` | `detect_namespace_conflicts`, `format_conflict_report` | Detects symbol collisions across donor trees |
| `orchestrator.py` | `rebuild_project`, `render_rebuild_summary`, `resolve_registry_inputs` | Top-level rebuild orchestrator |
| `forge.py` | `generate_plan`, `execute_plan`, `run_forge_phase`, `ForgeTask`, `ForgeResult` | Plan-then-execute forge loop |
| `version_tracker.py` | `assign_version`, `bump_version`, `classify_change`, `content_hash` | Semantic version tracking per atom |
| `project_parser.py` | `extract_symbols`, `classify_symbol`, `classify_tier`, `ingest_project` | Deep Python AST parser |
| `schema_materializer.py` | `materialize_plan`, `emit_certificate`, `canonical_name_for` | Phase 5: materializes CNA schemas to disk |
| `body_extractor.py` | `extract_body`, `enrich_components_with_bodies`, `derive_made_of_graph` | Extracts function/class bodies for synthesis |
| `cycle_detector.py` | `detect_cycles`, `break_cycles`, `validate_acyclic` | DAG cycle detection for import graphs |
| `coverage_emitter.py` | `emit_generated_quality_suite` | Generates test suites for emitted components |
| `finish.py` | `complete_function`, `scan_file`, `finish_project`, `IncompleteFunction` | Scans for NotImplementedError stubs and fills them |

---

## PRIORITY 2 — LLM Provider Stack (`ass-ade-v1/engine/`)
**Source:** `C:/!atomadic/ass-ade-v1/src/ass_ade/engine/`

| File | Symbols | Why |
|------|---------|-----|
| `provider.py` | `AnthropicProvider`, `OpenAICompatibleProvider`, `NexusProvider`, `MultiProvider` (with fallback) | Full LLM provider abstraction with hot-swap fallback |
| `tokens.py` | `TokenBudget`, `context_window_for`, `estimate_tokens`, `estimate_message_tokens` | Token counting + eviction planning for long runs |
| `registry.py` | `Registry` (vector search, embedding rerank), `scan_source_for_leaks`, `LeakHit` | Embedded symbol registry with semantic search + sovereignty leak detection |
| `scoring.py` | `score`, `select_best`, `runner_up_within_epsilon`, `ScoringConstants` | Confidence scoring with configurable weights |
| `fingerprint.py` | `sig_fp`, `body_fp`, `sig_fp_python`, `body_fp_python` | Content-addressed hashing for dedup/change detection |
| `nexus.py` | `NexusTransport`, `trust_receipt`, `nexus_preflight`, `TrustReceipt`, `PreflightResult` | Nexus transport with aegis/drift/hallucination checks |
| `types.py` | `AtomMetadata`, `AtomRef`, `AtomScore`, `BindPlan`, `LockFile`, `LockEntry`, `SovereignConstant`, `SovereignLeakError` | Core engine type system |
| `types_llm.py` | `CompletionRequest`, `CompletionResponse`, `Message`, `ToolCallRequest`, `ToolSchema` | Typed LLM request/response DTOs |
| `binder.py` | `bind` | Bind atom candidates to registry with dedup |
| `bindings_lock.py` | `read`, `write`, `verify` | Lock file for atomic binding operations |

---

## PRIORITY 3 — Swarm Bus (`ass-ade-v1/swarm/`)
**Source:** `C:/!atomadic/ass-ade-v1/src/ass_ade/swarm/`

| File | Symbols | Why |
|------|---------|-----|
| `bus.py` | `FileSignalBus` (broadcast, peek, inbox, ack, iter_log) | File-based signal bus for multi-agent coordination |
| `coordinator.py` | `SwarmCoordinator`, `TickResult` (halt, reroute, announce) | Tick-based swarm coordinator with halt/reroute logic |
| `protocol.py` | `parse_envelope`, `render_envelope`, `route_matches`, `serialize_envelope` | Signal serialization + routing protocol |
| `types.py` | `Signal`, `SignalEnvelope`, `Priority`, `AckRecord`, `DeliveryReceipt` | Typed swarm message primitives |

---

## PRIORITY 4 — MCP Server (`ass-ade-v1/mcp/`)
**Source:** `C:/!atomadic/ass-ade-v1/src/ass_ade/mcp/`

| File | Symbols | Why |
|------|---------|-----|
| `server.py` | `MCPServer` (full tool registry: phase0_recon, trust_gate, map_terrain, certify_output, context_memory, a2a, epiphany) | Exposes entire ASS-ADE as MCP server — the "ass-ade as MCP" feature |
| `zero_router.py` | `MCPZeroRouter`, `ToolRef` (discover, register, route, report) | Dynamic MCP tool discovery and zero-config routing |
| `cancellation.py` | `CancellationContext`, `NullCancellationContext` | Async cancellation support for long MCP calls |
| `utils.py` | `invoke_tool`, `resolve_tool`, `validate_payload`, `estimate_cost` | MCP tool invocation helpers |

---

## PRIORITY 5 — CLI Commands (`ass-ade-v1/commands/`)
**Source:** `C:/!atomadic/ass-ade-v1/src/ass_ade/commands/`

| File | Symbols | Why |
|------|---------|-----|
| `a2a.py` | `a2a_discover`, `a2a_negotiate`, `a2a_validate`, `register` | Agent-to-Agent protocol CLI |
| `providers.py` | `providers_list`, `providers_test`, `providers_set_key`, `providers_enable/disable` | Full provider management CLI |
| `workflow.py` | `workflow_phase0_recon`, `workflow_trust_gate`, `workflow_certify`, `workflow_map_terrain` | Workflow orchestration commands |
| `blueprint.py` | `build_blueprint`, `validate_blueprint`, `list_blueprints` | Blueprint management |
| `aso.py` | `optimize_codebase`, `optimize_swarm`, `optimize_context`, `optimize_telemetry` | ASO (Atomadic Swarm Optimization) commands |
| `agent.py` | `agent_chat`, `agent_run` | Agent interaction commands |

---

## PRIORITY 6 — v1.1 Phase Pipeline (`ass-ade-v1.1/a3_og_features/`)
**Source:** `C:/!atomadic/ass-ade-v1.1/src/ass_ade/a3_og_features/`

| File | Symbols | Why |
|------|---------|-----|
| `phase0_recon.py` | Full recon feature | Phase 0: repo reconnaissance |
| `phase1_ingest.py` | Ingest phase | Phase 1: symbol ingestion |
| `phase2_gapfill.py` | Gap fill phase | Phase 2: identify and fill gaps |
| `phase3_enrich.py` | Enrich phase | Phase 3: docstring/test enrichment |
| `phase4_validate.py` | Validate phase | Phase 4: validate emitted code |
| `phase5_materialize.py` | Materialize phase | Phase 5: write final files |
| `phase6_audit.py` | Audit phase | Phase 6: import law + sovereignty |
| `phase7_package.py` | Package phase | Phase 7: emit runnable package |
| `pipeline_book.py` | `PipelineBook` | Phase ledger tracking all phase results |

---

## PRIORITY 7 — v1.1 Pure Functions (`ass-ade-v1.1/a1_at_functions/`)
**Source:** `C:/!atomadic/ass-ade-v1.1/src/ass_ade/a1_at_functions/`

| File | Symbols | Why |
|------|---------|-----|
| `gap_fill.py` | gap fill helpers | Pure gap-fill logic (no state) |
| `conflict_detector.py` | conflict detection | Pure namespace conflict detection |
| `cycle_detector.py` | cycle detection | Pure DAG cycle detection |
| `ingest.py` | ingest helpers | Symbol ingestion helpers |
| `tier_purity.py` | tier purity checks | Pure tier validation |
| `assimilate_policy_gate.py` | policy gate | Policy enforcement at assimilation time |
| `assimilate_policy_plan.py` | policy planning | Build assimilation policy plans |
| `audit_rebuild.py` | audit helpers | Rebuild audit helpers |
| `cna_import_rewrite.py` | import rewriting | CNA-aware import rewriting |
| `body_extractor.py` | body extraction | Pure body extraction |
| `api_inventory_emit.py` | API inventory | Emit API inventory |
| `registry_fingerprint.py` | fingerprinting | Registry-level fingerprinting |
| `dotenv_bootstrap.py` | env bootstrap | .env loading helpers |

---

## PRIORITY 8 — Nexus Payment (`ass-ade-v1/nexus/`)
**Source:** `C:/!atomadic/ass-ade-v1/src/ass_ade/nexus/`

| File | Symbols | Why |
|------|---------|-----|
| `x402.py` | x402 USDC payment client | Autonomous micro-payment on Base L2 for Nexus calls |
| `client.py` | `NexusClient` | Full Nexus API client with resilience |
| `resilience.py` | circuit breaker, retry | Resilience patterns for Nexus calls |
| `validation.py` | response validation | Nexus response validation |
| `session.py` | session management | Nexus session handling |

---

## PRIORITY 9 — Feature Layer (`ass-ade-v1/a3_og_features/`)
**Source:** `C:/!atomadic/ass-ade-v1/src/ass_ade/a3_og_features/`

| File | Symbols | Why |
|------|---------|-----|
| `epiphany_engine.py` | `EpiphanyEngine` (plan, run_recon, generate_breakthrough, check_promotion) | AI-driven breakthrough detection |
| `forge_loop.py` | `ForgeLoop` (run_full, run_plan, verify, record_episode, propose_goals) | Full forge execution loop |
| `auth_gate.py` | `require_premium`, `log_usage`, `PremiumGateError` | Premium feature gating |
| `context_pack_builder.py` | `build_context_pack` | Build context packs for LLM calls |

---

## PRIORITY 10 — A2A + Protocol (`ass-ade-v1/`)
**Source:** `C:/!atomadic/ass-ade-v1/src/ass_ade/`

| File | Symbols | Why |
|------|---------|-----|
| `protocol/cycle.py` | `ProtocolAssessment`, `ProtocolAuditCheck` | Protocol compliance assessment |
| `protocol/evolution.py` | evolution cycle | Protocol evolution tracking |
| `context_memory.py` | context memory system | Persistent context between sessions |
| `map_terrain.py` | `map_terrain` | Terrain mapping command |

---

## ALSO NOTED — Orphan Tree (`!ass-ade-cursor-dev-20260420-1710`)
**Source:** `C:/!aaaa-nexus/!ass-ade-cursor-dev-20260420-1710/merged/src/ass_ade/`

| File | Symbols | Why |
|------|---------|-----|
| `engine/rebuild/native_wire.py` | `rewrite_shadow_stubs` (Phase 0.5), `emit_native_package` (Phase 5.5), `NativeSource` | Two-half bridge: replaces stubs BEFORE Phase 1, emits native packages AFTER Phase 5 |
| `runtime/bridge.py` | `call_native`, `BridgeError` | JSON-RPC 2.0 subprocess dispatcher for Rust/TS/Kotlin/Swift |

---

## Quick-Start Commands

```bash
# Scan and cherry-pick the rebuild engine (86 symbols):
ass-ade cherry-pick "C:/!atomadic/ass-ade-v1/src/ass_ade/engine/rebuild" --target . --pick all --no-interactive

# Assimilate into monadic tiers:
ass-ade assimilate --dry-run   # preview
ass-ade assimilate             # write to tier dirs

# Scan v1.1 pipeline phases:
ass-ade cherry-pick "C:/!atomadic/ass-ade-v1.1/src/ass_ade/a3_og_features" --target . --pick all --no-interactive

# Scan swarm bus:
ass-ade cherry-pick "C:/!atomadic/ass-ade-v1/src/ass_ade/swarm" --target . --pick all --no-interactive

# Scan MCP server:
ass-ade cherry-pick "C:/!atomadic/ass-ade-v1/src/ass_ade/mcp" --target . --pick all --no-interactive
```

---

## Estimated Scope

| Priority | Source Dir | Symbols | Tier Destination |
|----------|-----------|---------|-----------------|
| 1 | engine/rebuild/ | 86 | a1 (pure fns) + a2 (classes) |
| 2 | engine/ (non-rebuild) | 135 | a1 + a2 |
| 3 | swarm/ | 41 | a1 + a2 |
| 4 | mcp/ | 58 | a2 + a3 |
| 5 | commands/ | 39 | a4 |
| 6 | v1.1 phases | ~80 | a3 |
| 7 | v1.1 a1 funcs | ~60 | a1 |
| 8 | nexus/ | ~40 | a1 + a2 |
| 9 | a3_og_features/ | 16 | a3 |
| 10 | orphan native_wire | 5 | a1 + a2 |
| **TOTAL** | | **~560** | |
