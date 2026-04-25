# Public and Private RAG

For a non-technical explanation of RAG, vectors, context, and private/public
memory, start with [GLOSSARY.md](GLOSSARY.md).

ASS-ADE has two retrieval surfaces with different trust boundaries:

- **Public/local RAG:** repo-local context packets and deterministic vector memory.
- **Private/owner RAG:** Atomadic private knowledge-base search through
  AAAA-Nexus internal endpoints.

Both are wired into the current CLI. The local surface is also exposed through
MCP.

## Current Wiring

| Surface | Status | Entrypoints | Backing store |
|---------|--------|-------------|---------------|
| Public context packets | Wired | `ass-ade context pack`, MCP `context_pack` | Selected repo files and Phase 0 recon output |
| Public local vector memory | Wired | `ass-ade context store`, `ass-ade context query`, MCP `context_memory_store`, MCP `context_memory_query` | `.ass-ade/vector-memory/vectors.jsonl` under the target working directory |
| Private Atomadic RAG | Wired client path | `ass-ade search`, `ass-ade search --chat` | Remote owner-only AAAA-Nexus private knowledge base |
| Registry semantic lookup | Present, default-off | `Registry.search_by_embedding`, `Registry.retrieve_then_rerank` | `.ass-ade/registry/symbols.jsonl` rows with caller-supplied embeddings |
| Pluggable vector DB adapters | Pending | none | candidate files exist, not active |

## Public Local RAG

The public surface lives in `src/ass_ade/context_memory.py`. It is designed to be
safe in the open-source seed:

- No network calls.
- No private Atomadic corpus access.
- No external embedding model required.
- Deterministic signed hashing vectors.
- Repo-relative file reads guarded against path escape.
- JSONL persistence under the working directory.

Store trusted text:

```powershell
python -m ass_ade context store "trusted docs packet" --namespace demo --path . --json
```

Query trusted text:

```powershell
python -m ass_ade context query "trusted docs" --namespace demo --path . --json
```

Build a context packet from files and already-researched source URLs:

```powershell
python -m ass_ade context pack "Add an MCP tool schema" `
  --file src\ass_ade\mcp\server.py `
  --source https://modelcontextprotocol.io/specification/2025-11-25/server/tools `
  --path . `
  --json
```

The context packet uses `phase0_recon` to decide whether the task is ready or
needs more external source research. It records file hashes and excerpts so
agents can work from evidence instead of vague memory.

## MCP Exposure

The local RAG tools are present in `mcp/server.json` and implemented in
`src/ass_ade/mcp/server.py`:

- `context_pack`
- `context_memory_store`
- `context_memory_query`

These are local tools. They do not call the private knowledge base and do not
need `AAAA_NEXUS_API_KEY`.

## Private Owner RAG

The private RAG client path is intentionally separate:

```powershell
$env:AAAA_NEXUS_BASE_URL="https://atomadic.tech"
$env:AAAA_NEXUS_API_KEY="<api key if required by the configured endpoint>"
$env:ATOMADIC_SESSION_TOKEN="<owner session token>"

python -m ass_ade search "Atomadic invariants" --max-results 10
python -m ass_ade search "Atomadic invariants" --chat
```

The CLI command is `search` in `src/ass_ade/cli.py`. It requires
`ATOMADIC_SESSION_TOKEN` and calls:

- `NexusClient.internal_search(...)` -> `POST /internal/search`
- `NexusClient.internal_search_chat(...)` -> `POST /internal/search/chat`

The session token is sent as `X-Owner-Token` after header sanitization. Search
results are printed as JSON. The private corpus stays remote; it is not copied
into `.ass-ade/vector-memory`.

## Registry Semantic Lookup

The registry has semantic lookup hooks, but they are not the general RAG path.
They are default-off and require caller-supplied vectors:

```powershell
$env:ATOMADIC_USE_EMBEDDINGS="1"
```

Relevant code:

- `src/ass_ade/a2_mo_composites/registry_core.py`
- `src/ass_ade/a1_at_functions/search_by_embedding_helpers.py`
- `src/ass_ade/a1_at_functions/retrieve_then_rerank_helpers.py`

The registry does not load an embedding model. It only compares vectors already
stored in registry metadata.

## Worktree Findings

Current worktrees:

- `.claude/worktrees/confident-spence-f44d27`
- `.claude/worktrees/modest-williams-b4f42e`

Neither worktree contains committed diffs to the wired RAG files
`context_memory.py`, `nexus/client.py`, `mcp/server.py`, or `cli.py`.

One worktree contains `src/ass_ade/a1_at_functions/research_harvester.py`, which
extracts decisions, actions, questions, ideas, and risks from text. It is not in
the seed trunk and is not wired into the current RAG flow. Treat it as a scout
or cherry-pick candidate, not as active product terrain.

## Pending Artifacts

These files are present in the working tree but are not active RAG wiring:

- `src/ass_ade/vector_db_backend.py`
- `src/ass_ade/tokenizer_memory_adapter.py`
- `src/ass_ade/prompt_chaining.py`

They are not imported by production code, not covered by tests in this checkout,
and are tracked as pending in `CHERRY_PICKING_SHOPPING_LIST.md`. Before they can
be promoted, they need a real design pass, tests, CLI or MCP exposure, and no
placeholder behavior.

## Validation

Run the existing coverage for the live RAG surfaces:

```powershell
python -m pytest tests\test_recon_context.py tests\test_search_x402.py
python -m ass_ade context --help
python -m ass_ade search --help
```
