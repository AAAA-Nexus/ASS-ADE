# ASS-ADE Evolution & Integration Plan

## Current RAG Baseline

- Public/local RAG is wired through `src/ass_ade/context_memory.py`, CLI
  `context pack/store/query`, and MCP `context_pack`,
  `context_memory_store`, and `context_memory_query`.
- Private owner RAG is wired through CLI `search` and
  `NexusClient.internal_search*`, which call AAAA-Nexus internal search
  endpoints with `ATOMADIC_SESSION_TOKEN`.
- Pluggable vector DB, tokenizer adapter, and prompt-chaining files currently in
  the working tree are candidates, not active product terrain. Promote them only
  after tests, CLI/MCP exposure, and no placeholder behavior.

## 1. LoRA-Based Self-Improvement Expansion
- Extend LoRA Flywheel to support multi-agent, multi-session learning
- Enable cross-agent principle sharing and feedback
- Add hooks for continual learning pipelines (RLHF, OpenChatKit-style)

## 2. Pluggable Vector DB Integration
- Abstract vector memory backend (Chroma, Qdrant, Weaviate, etc.)
- Add config for local/remote vector DB selection
- Implement adapters for at least one open-source vector DB

## 3. Dynamic Prompt Chaining & Live Editing
- Implement prompt chaining and retrieval-augmented prompt construction
- Add UI hooks for live prompt editing and context injection
- Support dynamic prompt templates per agent/task

## 4. Dashboard for Agent/Memory/Prompt Monitoring
- Build real-time dashboard (Streamlit/Gradio/React)
  - Agent status, memory, and context inspection
  - Live prompt editing and preview
  - LoRA/contribution stats and wisdom/principle tracking
  - Delegation depth and orchestration visualization

## 5. Immediate Cherry-Pick Targets
- Vector DB adapters from open-source (Chroma, Qdrant, etc.)
- Tokenizer libraries for model-aligned token counting
- Dashboard components from Streamlit/Gradio
- Prompt chaining/RAG patterns from LangChain/Haystack

---

### Next Steps
- [ ] Implement vector DB backend abstraction and config
- [ ] Add dashboard project skeleton
- [ ] Add prompt chaining and live editing through real CLI/MCP/dashboard surfaces
- [ ] Expand LoRA Flywheel for multi-agent learning
- [ ] Integrate tokenizer and memory adapters
