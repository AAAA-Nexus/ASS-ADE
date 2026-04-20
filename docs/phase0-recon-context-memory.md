# Phase 0 Recon And Context Memory

ASS-ADE now treats **Never Code Blind** as an executable Phase 0 gate.
Technical tasks must start with local codebase recon and current source targets
before capability planning, code synthesis, or MCP calls that mutate state.

## Executable Tools

| Surface | Tool | Purpose |
| --- | --- | --- |
| CLI | `ass-ade workflow phase0-recon` | Inspect the repo and require latest technical-document source URLs. |
| MCP | `phase0_recon` | Same gate for MCP clients. Returns `RECON_REQUIRED` until sources and relevant files are present. |
| CLI | `ass-ade context pack` | Build a compact prompt-ready packet from repo files and source URLs. |
| MCP | `context_pack` | Same packet builder for MCP clients. |
| CLI | `ass-ade context store` | Store trusted text in local vector memory. |
| CLI | `ass-ade context query` | Recall trusted text from local vector memory. |
| MCP | `context_memory_store` / `context_memory_query` | MCP-accessible local vector memory. |

## Phase Order

```text
Phase 0-A: Recon
  -> inspect repo
  -> identify relevant files
  -> require current official docs for technical dependencies

Phase 0-B: Context Packet
  -> combine source URLs and repo excerpts
  -> hash included files
  -> emit warnings if source freshness is missing

Phase 0-C: Context Memory
  -> store trusted packets or task lessons
  -> query prior relevant packets

Phase 1+: MAP = TERRAIN
  -> only after recon/context gates are satisfied
```

## Local Vector Memory

The local vector memory uses a deterministic signed hashing projection. The
public contract is intentionally generic: callers store trusted text, attach
metadata, and query relevant memories without learning private retrieval
internals.

Stored records live under:

```text
.ass-ade/vector-memory/vectors.jsonl
```

Each record includes:

- namespace
- text
- normalized vector
- metadata
- timestamp
- stable local record ID

## Examples

Run Phase 0 recon:

```powershell
python -m ass_ade workflow phase0-recon `
  "Add an MCP tool schema" `
  --source https://modelcontextprotocol.io/specification/2025-11-25/server/tools `
  --json
```

Build a context packet:

```powershell
python -m ass_ade context pack `
  "Add an MCP tool schema" `
  --file src/ass_ade/mcp/server.py `
  --source https://modelcontextprotocol.io/specification/2025-11-25/server/tools `
  --json
```

Store and query trusted memory:

```powershell
python -m ass_ade context store "MCP tools require inputSchema and tool names." --namespace mcp
python -m ass_ade context query "tool schema" --namespace mcp --json
```

## Hosted Follow-Up

The local memory is the free/public substrate. The enterprise path should
replace or augment it with:

- `nexus_trusted_rag_augment`
- `nexus_embed`
- `nexus_vq_memory_query`
- `nexus_vq_memory_store`
- provenance ranker
- hallucination oracle gating
- shared LoRA training packet generation
