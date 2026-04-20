# Trust-Gated RAG And Shared LoRA Flywheel

This is the primary compounding advantage for ASS-ADE Enterprise: millions of
developer agents feeding one trust-gated knowledge loop that improves small
models through shared adapters.

The goal is not to promise flawless code. The goal is to make every accepted
training sample provenance-bearing, verified, reproducible, privacy-scrubbed,
and eval-positive so a 3B-8B model can become dramatically better at the
actual workflows ASS-ADE performs.

## Core Thesis

```text
trusted docs + repo context
  -> trust-gated RAG packet
  -> verified task execution
  -> high-quality fix/sample capture
  -> privacy scrub + provenance hash
  -> shared LoRA training queue
  -> eval-gated adapter promotion
  -> all agents retrieve better adapters
  -> better executions create better samples
```

At very high scale, the power comes from selective pressure. Ten million agents
can create noise quickly; the system only improves if bad samples are cheaper to
reject than good samples are to promote.

## Cloudflare Responsibilities

| Component | Cloudflare Primitive | Responsibility |
| --- | --- | --- |
| Trust RAG Worker | Workers | Accept task/context requests, apply gates, return grounded packets. |
| Global Registry | D1 | Store documents, agent IDs, adapter metadata, eval scores, rewards. |
| Semantic Memory | Vectorize | Query trusted docs, code patterns, task traces, and fix exemplars. |
| Document Corpus | R2 | Store raw docs, normalized docs, redacted traces, training artifacts. |
| Coordination | Durable Objects | Deduplicate contributions, buffer LoRA batches, coordinate training states. |
| Ledger | Durable Objects + D1 | Idempotent reward claims, lineage receipts, usage accounting. |
| Queue | Queues | Async scrub, eval, train, promote, rollback jobs. |

## Trust-Gated RAG Agent

The RAG agent is the front door. It decides what knowledge is allowed to guide
code generation or become a training candidate.

Required gates:

1. **Source gate**: official docs, repo-local files, signed internal docs, or
   whitelisted trusted publishers.
2. **Freshness gate**: technical docs must satisfy the configured freshness SLA.
3. **Provenance gate**: every chunk carries source URL/path, retrieval time,
   content hash, and normalization version.
4. **Security gate**: no secrets, tokens, private customer data, or internal-only
   prompts enter the packet.
5. **Relevance gate**: source relevance must beat a minimum threshold against
   the task and repo recon.
6. **Hallucination gate**: generated summaries must be certifiable against the
   retrieved chunks.
7. **License gate**: content must be allowed for the intended use.
8. **Tau gate**: Nexus trust/tau rating must meet the configured threshold for
   high-impact memory writes or LoRA contributions.
9. **Drift gate**: Nexus drift protection must reject context that would move
   the agent away from the task, repo state, or verified source packet.

If any required gate, tool, skill, agent, or harness does not exist, the
workflow returns to `map_terrain` and produces a capability development plan
before the original task may continue.

Local ASS-ADE feeder tools:

- `phase0_recon`
- `context_pack`
- `context_memory_store`
- `context_memory_query`

Hosted enterprise tools:

- `nexus_trusted_rag_augment`
- `nexus_embed`
- `nexus_vq_memory_query`
- `nexus_vq_memory_store`
- `nexus_hallucination_oracle`
- `nexus_memory_trim`

## Shared LoRA Mesh

The Shared LoRA Mesh consumes only high-quality execution artifacts.

Accepted sample types:

- bug/fix pairs with passing regression tests
- prompt/context/result triples with citations
- failing test to passing implementation traces
- verified MCP tool schemas and handlers
- security patches with scan evidence
- refactors with before/after performance or maintainability evidence

Rejected sample types:

- unverifiable answers
- code without tests or review evidence
- samples containing secrets or private data
- speculative claims without source grounding
- license-unsafe content
- duplicate low-value traces

Promotion gates:

1. Adapter trains on a sealed batch with dataset hash.
2. Eval suite runs on held-out tasks, golden fixtures, and regression packs.
3. Adapter must improve target workflows without regressing safety or baseline
   code quality.
4. Canary rollout starts with low-risk agent cohorts.
5. Bad adapters are rolled back and permanently tagged with failure reasons.

## Minimal Schemas

Trust RAG packet:

```json
{
  "packet_id": "rag_...",
  "task_hash": "sha256...",
  "sources": [
    {
      "uri": "https://modelcontextprotocol.io/specification/2025-11-25/server/tools",
      "retrieved_at": "2026-04-17T00:00:00Z",
      "content_hash": "sha256...",
      "trust_score": 0.99,
      "license": "docs-allowed"
    }
  ],
  "chunks": [
    {
      "chunk_id": "chunk_...",
      "source_uri": "https://...",
      "text_hash": "sha256...",
      "summary": "MCP tools require a valid object inputSchema.",
      "relevance_score": 0.94
    }
  ],
  "verdict": "TRUSTED"
}
```

LoRA contribution:

```json
{
  "contribution_id": "lora_...",
  "agent_id": "agent_...",
  "base_model": "qwen3-3b",
  "task_class": "mcp_tool_implementation",
  "rag_packet_id": "rag_...",
  "diff_hash": "sha256...",
  "test_evidence_hash": "sha256...",
  "quality_score": 0.998,
  "privacy_scrubbed": true,
  "license_safe": true
}
```

Adapter registry row:

```json
{
  "adapter_id": "adapter_...",
  "base_model": "qwen3-3b",
  "dataset_hash": "sha256...",
  "eval_score": 0.91,
  "safety_score": 0.99,
  "status": "canary",
  "created_at": "2026-04-17T00:00:00Z"
}
```

## Implementation Order

1. Wire local feeder tools into every coding workflow:
   `phase0_recon -> context_pack -> map_terrain`.
2. Build hosted `nexus_trusted_rag_augment` contract with provenance and
   hallucination gates.
3. Store accepted packets in R2 and embeddings in Vectorize.
4. Add `nexus_lora_capture_fix` as a local-first buffer with privacy scrub.
5. Add Durable Object batcher for idempotent contribution aggregation.
6. Add adapter registry in D1 with model checksum, dataset hash, eval score,
   rollout state, and rollback reason.
7. Build eval gate before any adapter can become default.
8. Add reward ledger only after quality gates are stable.

## Scale Target

At 10 million agents, the winning architecture is not “train on everything.”
It is:

- reject aggressively
- deduplicate aggressively
- reward only verified novelty
- promote only eval-positive adapters
- keep every adapter rollbackable
- keep every sample traceable

That is how the Hive turns volume into capability instead of entropy.
