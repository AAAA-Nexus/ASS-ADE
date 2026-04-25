# Atomadic RAG: Public and Private Memory

Atomadic has two complementary RAG (Retrieval-Augmented Generation) systems — one public, one private — giving you the best of open transparency and confidential depth.

## Public RAG — `context` commands

Public RAG is your shareable, session-scoped memory. It holds context packs that any Atomadic agent can read.

```bash
# Pack current session context into a shareable bundle
atomadic context pack

# Store content into the public vector memory
atomadic context store "Your insight or document text here"

# Query public vector memory
atomadic context query "What do we know about monadic tiers?"
```

Public RAG data lives in `.ass-ade/vector-memory/` and is indexed by the local Chroma/FAISS store.

### When to use public RAG
- Sharing context between team members
- Storing project documentation for agent retrieval
- Building a shared knowledge base for the Atomadic swarm
- Seeding the Epiphany Engine with scout reports

## Private RAG — `search --chat`

Private RAG is your confidential, deep-search memory backed by the AAAA-Nexus private knowledge base. It is not shared — it belongs to your Atomadic session.

```bash
# Search private knowledge base (read-only)
atomadic search "Atomadic launch strategy"

# Search with LLM-generated answer
atomadic search "How does x402 work?" --chat
```

Private RAG is backed by the AAAA-Nexus Cloudflare Vectorize + AutoRAG index at `atomadic.tech`. It requires a valid `AAAA_NEXUS_API_KEY`.

### When to use private RAG
- Retrieving Thomas's private research notes
- Querying confidential business context
- Asking Atomadic to synthesize private knowledge with current terrain
- Feeding the Sovereign Epiphany Engine with private signals

## Architecture

```
Public RAG                          Private RAG
──────────────────────────────      ──────────────────────────────────
context pack → .ass-ade/packs/      AAAA_NEXUS_API_KEY → atomadic.tech
context store → vector-memory/      Cloudflare AutoRAG + Vectorize
context query ← local Chroma        search --chat ← /v1/rag/augment
MAP = TERRAIN enforced               MAP = TERRAIN enforced
```

## Trust Model

Both RAG systems are gated by MAP = TERRAIN:
- Retrieved content is labelled **VERIFIED** (from stored sources) or **INFERRED** (LLM synthesis over retrievals)
- No hallucinated citations — every retrieval is grounded in indexed documents
- Public RAG is auditable by lineage; private RAG is confidential by design

## Vectorize Index (Storefront)

The private RAG storefront exposes:

| Route | Purpose |
|---|---|
| `POST /v1/rag/augment` | Query + LLM-augment a prompt with retrieved context |
| `POST /v1/rag/index` | Index a new document into Cloudflare Vectorize |

Both routes require `Authorization: Bearer <AAAA_NEXUS_API_KEY>` and `CF_AI_TOKEN` (server-side secret for Cloudflare Workers AI).

## Environment Variables

| Variable | Where | Purpose |
|---|---|---|
| `AAAA_NEXUS_API_KEY` | Client `.env` | Auth token for private RAG API |
| `CF_AI_TOKEN` | Cloudflare secret | Cloudflare Workers AI token |
| `CF_VECTORIZE_TOKEN` | Cloudflare secret | Cloudflare Vectorize write token |

Set Cloudflare secrets via:
```bash
wrangler secret put CF_AI_TOKEN
wrangler secret put CF_VECTORIZE_TOKEN
```
