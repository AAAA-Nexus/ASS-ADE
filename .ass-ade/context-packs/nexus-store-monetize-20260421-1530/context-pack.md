# Context pack — Nexus MCP + atomadic.tech monetization

## Intent

Improve **hosted MCP** on `https://atomadic.tech/mcp` (and related `/.well-known/*` routes) and **monetize** through **x402**, **API keys**, and existing **Stripe** flows already wired in the Worker. This pack supports implementation under Atomadic **MAP=TERRAIN** (repo paths first, web specs second).

## Repo map (Lane L)

- **Routing:** `!aaaa-nexus-storefront/src/router.rs` — `/mcp`, well-known MCP/OAuth paths, marketing vs paid classification.
- **Dispatch:** `!aaaa-nexus-storefront/src/lib.rs` — MCP JSON-RPC responses, install docs, references to `serverUrl` `https://atomadic.tech/mcp`.
- **Payments:** `!aaaa-nexus-storefront/src/payments.rs`, `crates/nexus-pay/src/x402.rs` — x402-style `PAYMENT-*` headers and errors.
- **Premium proxy:** `!aaaa-nexus-storefront/src/aegis.rs` — `POST /v1/aegis/mcp-proxy/execute` (priced in `utils.rs`).
- **Developer MCP (stdio):** `!ass-ade/mcp/server.json` + `src/ass_ade/mcp/server.py` — must stay in sync with **manifest parity** tests.

## Web research (Lane W)

- **MCP HTTP authorization (2025-11-25):** [Authorization spec](https://modelcontextprotocol.io/specification/2025-11-25/basic/authorization) — use for OAuth metadata and HTTP MCP hardening.
- **x402 HTTP 402:** [docs.x402.org — HTTP 402](https://docs.x402.org/core-concepts/http-402) — V2 `PAYMENT-REQUIRED`, `PAYMENT-SIGNATURE`, `PAYMENT-RESPONSE`.
- **Cloudflare remote MCP:** [Cloudflare blog — Remote MCP servers](https://blog.cloudflare.com/remote-model-context-protocol-servers-mcp) — edge deployment patterns.
- **Hop 1b — AI modality:** [MCPAgentBench arXiv](https://arxiv.org/abs/2512.24565) — tool overload / distractors; keep **narrow, priced** MCP SKUs.

## Tech docs (Lane T)

- **Worker:** `wrangler.toml` — routes `atomadic.tech/*`, public `STRIPE_PUBLIC_KEY`, secrets via `wrangler secret put`.
- **MCP protocol version:** `mcp/server.json` declares `"protocol": "2025-11-25"`.

## Risks / gaps

- Revenue velocity is an **[H]** business metric — needs analytics, not only code.
- Full OAuth E2E needs secrets and staging IdP — **[S]** quarantine until staffed.

## Next edits (for dev agent)

1. Trace `/mcp` request path in `lib.rs` → enforce **402** + OAuth discovery headers per spec.
2. Run **T5** diff: `nexus-pay` vs x402 docs; add tests if wire format drifts.
3. Extend **pricing** surfaces (`/.well-known/pricing.json` if present) to list **per-tool** costs for MCP `tools/list` consumers.

## Pack verdict

**PASS** — Lanes L/W/T merged; hops include **H1b**; `verificationEvidence` points to fetched URLs and concrete repo paths.
