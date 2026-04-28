# Atomadic Cherry Picking Shopping List

This document tracks high-value features, functions, and modules to cherry-pick and assimilate into Atomadic (ASS-ADE).

## How to use
- Add any feature, function, or module from any sibling or legacy ASS-ADE/Atomadic repo that should be assimilated.
- Include a short description and the source path if possible.
- Mark status: [pending], [in progress], [done], [skipped]

---

## Cherry Picking Candidates

| Feature/Function/Module | Description | Source Path | Status |
|------------------------|-------------|-------------|--------|
| **PRIORITY 1: Multilang Rebuild Engine** | Gap fill, bridge emitters, synthesis, tier purity, orchestrator, etc. | See .ass-ade/launch_day_shopping_list.md | [pending] |
| **PRIORITY 2: LLM Provider Stack** | Provider abstraction, token budgeting, registry, scoring, fingerprinting, Nexus transport | See .ass-ade/launch_day_shopping_list.md | [pending] |
| **PRIORITY 3: Swarm Bus/Coordinator** | Multi-agent coordination, protocol, message primitives | See .ass-ade/launch_day_shopping_list.md | [pending] |
| **PRIORITY 4: MCP Server/Tool Registry** | Expose all agent tools via MCP, dynamic tool discovery | See .ass-ade/launch_day_shopping_list.md | [pending] |
| **PRIORITY 5: CLI Commands** | Unified CLI for cherry-pick, assimilate, rebuild, enhance, agent chat, etc. | See .ass-ade/launch_day_shopping_list.md | [pending] |
| **PRIORITY 6: v1.1 Phase Pipeline** | Recon, ingest, gapfill, enrich, validate, materialize, audit, package | See .ass-ade/launch_day_shopping_list.md | [pending] |
| **PRIORITY 7: Pure Function Helpers** | Gap fill, conflict/cycle detection, policy gates, audit, import rewriting, etc. | See .ass-ade/launch_day_shopping_list.md | [pending] |
| **PRIORITY 8: Nexus Payment/Client** | Payment client, API client, resilience, validation, session | See .ass-ade/launch_day_shopping_list.md | [pending] |
| **PRIORITY 9: Feature Layer** | Epiphany engine, forge loop, premium gating, context pack builder | See .ass-ade/launch_day_shopping_list.md | [pending] |
| **PRIORITY 10: Protocol/Context/Compliance** | Protocol compliance, context memory, terrain mapping, audit, lineage | See .ass-ade/launch_day_shopping_list.md | [pending] |
| **LangChain Prompt Chaining** | Dynamic prompt chaining, retrieval-augmented generation, agent toolkits | https://github.com/langchain-ai/langchain | [pending] |
| **Haystack RAG Pipelines** | Modular RAG pipelines, vector DB adapters, prompt templates | https://github.com/deepset-ai/haystack | [pending] |
| **Chroma Vector DB** | Open-source vector DB, Python API, persistent/ephemeral modes | https://github.com/chroma-core/chroma | [pending] |
| **Qdrant Vector DB** | High-performance vector search, REST/gRPC, hybrid search | https://github.com/qdrant/qdrant | [pending] |
| **Gradio Dashboard Components** | Real-time dashboards, UI for agent status, memory, prompt editing | https://github.com/gradio-app/gradio | [pending] |
| **Streamlit Dashboard** | Python-native dashboards, live data, agent orchestration UI | https://github.com/streamlit/streamlit | [pending] |
| **OpenChatKit RLHF/LoRA** | RLHF, LoRA, multi-agent learning, open-source training recipes | https://github.com/togethercomputer/OpenChatKit | [pending] |
| **FastAPI Orchestration** | Async API orchestration, background tasks, agent endpoints | https://github.com/tiangolo/fastapi | [pending] |
| **EU AI Act Compliance Tools** | Open compliance checklists, drift/fairness audits | https://github.com/LAION-AI/Open-Assistant | [pending] |
| **Trust/Lineage Receipts** | Tamper-evident trust receipts, audit trails, agent reputation | https://github.com/atomadic/aaaa-nexus (see TrustReceipt, trust_chain_sign) | [pending] |
| **LoRA Flywheel Expansion** | Multi-agent LoRA flywheel, continual learning, cross-agent feedback | scripts/lora_training/train_lora.py, scripts/hf_space/app.py | [pending] |
| **Tokenizer Memory Adapter** | Model-aligned token counting, memory-efficient adapters | src/ass_ade/tokenizer_memory_adapter.py | [pending: not wired] |
| **Public Local RAG** | Context packets and deterministic local vector memory | src/ass_ade/context_memory.py, CLI `context`, MCP `context_*` tools | [done] |
| **Private Owner RAG** | Owner-only private knowledge-base search via Nexus internal endpoints | src/ass_ade/cli.py `search`, src/ass_ade/nexus/client.py `internal_search*` | [done: client-wired] |
| **Self-Healing Enforcement** | CLI self-healing, missing command auto-creation | Policy: see user memory notes | [pending] |
| **Agent Swarm Protocols** | Multi-agent coordination, signal bus, protocol compliance | src/ass_ade/swarm/, agents/_PROTOCOL.md | [pending] |
| **Blueprint/Feature Proposals** | AAAA-SPEC-004 blueprints, feature decomposition, plan emit | src/ass_ade/commands/feature.py, docs/ASS_ADE_FEATURE_INVENTORY.md | [pending] |
| **Dynamic Capability Inventory** | Live CLI/agent/tool registry, prompt-injected capabilities | agents/atomadic_interpreter.md | [pending] |
| **Compliance/Trust Gates** | Multi-step trust gating, hallucination oracles, drift checks | src/ass_ade/agent/trust_gate.py, src/ass_ade/a1_at_functions/trust_receipt_helpers.py | [pending] |
| **MCP Server/Tool Registry** | Expose all agent tools via MCP, dynamic tool discovery | src/ass_ade/mcp/, src/ass_ade/commands/mcp.py | [pending] |
| **A2A Protocol/Validation** | Agent-to-agent negotiation, validation, registry | src/ass_ade/commands/a2a.py, agents/08-canonical-name-authority.prompt.md | [pending] |
| **RLHF/LoRA Training Recipes** | HuggingFace, PEFT, Unsloth, LlamaFactory integration | scripts/lora_training/train_lora.py, scripts/hf_space/app.py | [pending] |
| **Orchestration/Assimilation CLI** | Unified CLI for cherry-pick, assimilate, rebuild, enhance | src/ass_ade/cli.py, src/ass_ade/commands/cherry.py, src/ass_ade/commands/assimilate.py | [pending] |
| **Agentic Dashboard** | Real-time agent/memory/prompt dashboard, live editing | (see Gradio/Streamlit above) | [pending] |
| **Prompt/Blueprint Live Editing** | UI hooks for prompt/blueprint editing, context injection | (see dashboard, LangChain, Haystack) | [pending] |
| **Vector DB Adapters** | Pluggable adapters for Chroma, Qdrant, Weaviate | src/ass_ade/vector_db_backend.py | [pending: not wired] |
| **Token Budgeting/Counting** | Model-aligned token budgeting, eviction planning | src/ass_ade/engine/tokens.py | [pending] |
| **Semantic Search/Registry** | Embedded symbol registry, semantic search, leak detection | src/ass_ade/engine/registry.py | [pending] |
| **Confidence Scoring** | Configurable scoring, best/runner-up selection | src/ass_ade/engine/scoring.py | [pending] |
| **Content-Addressed Hashing** | sig_fp, body_fp, deduplication, change detection | src/ass_ade/engine/fingerprint.py | [pending] |
| **Nexus Transport/Trust** | Nexus API client, trust receipts, drift/hallucination checks | src/ass_ade/engine/nexus.py | [pending] |
| **Blueprint Management** | Build, validate, list blueprints, plan emit | src/ass_ade/commands/blueprint.py | [pending] |
| **Swarm Bus/Coordinator** | File-based signal bus, tick-based coordination | src/ass_ade/swarm/bus.py, src/ass_ade/swarm/coordinator.py | [pending] |
| **Protocol Compliance Assessment** | Protocol assessment, evolution tracking | src/ass_ade/protocol/cycle.py, src/ass_ade/protocol/evolution.py | [pending] |
| **Context Memory System** | Persistent context, context pack builder | src/ass_ade/context_memory.py, src/ass_ade/cli.py `context`, src/ass_ade/mcp/server.py `context_*` | [done] |
| **Materializer/IDE Integration** | ADE materializer, cross-IDE hooks, VS Code/Cursor support | src/ass_ade/ade/materialize.py, docs/ASS_ADE_UNIFICATION.md | [pending] |
| **Audit/Lineage/Compliance** | Tamper-evident audit, compliance, and lineage records | src/ass_ade/ade/staging_handoff.py, src/ass_ade/agent/cie.py | [pending] |

---

Add new rows as you discover more candidates. Use this as the single source of truth for Atomadic feature assimilation.
