# ASS-ADE swarm — AAAA-Nexus MCP binding (operational)

**Companion:** `<ATOMADIC_WORKSPACE>/agents/_PROTOCOL.md` §11. This document is the **Cursor-facing tool matrix** (names, order, server id). If `_PROTOCOL.md` and this file disagree on policy, **`_PROTOCOL.md` wins`. For **where code may live**, **CNA ids**, and **standard tier terminology** (QK / atom / molecular / organic / synthesis) in `ass_ade`, see **`<ATOMADIC_WORKSPACE>/agents/ASS_ADE_MONADIC_CODING.md`** first.

**MANDATORY (operator / authorized `AAAA_NEXUS_API_KEY`):** If you control AAAA-Nexus and have a **valid key** (including no effective billing barrier for your account), you **always** run the **full** preflight and postflight tool chain for every ASS-ADE swarm turn — `uep_preflight`, Aegis, drift/trust, hallucination, ratchet/lineage as required by §11. **Do not** skip Nexus “to save µUSDC” or time when the key is available; the swarm is **governed** on purpose. The **host** agent completes the HTTPS follow-up (invocation contract) and **attaches** receipts to every Task subagent handoff.

**MCP server (Cursor):** `user-aaaa-nexus`  
Read tool JSON schemas from the workspace `mcps/user-aaaa-nexus/tools/<toolName>.json` before every `call_mcp_tool` invocation. The remote may return an invocation contract and **402 Payment Required** on the target HTTP route — complete payment per the challenge and `rules/aaaa-nexus-payment-posture.mdc` on the AAAA-Nexus plugin. Never log secrets (`rules/aaaa-nexus-usage.mdc`).

**API keys (Atomadic layout):** The canonical file is **`<ATOMADIC_WORKSPACE>/.env`** (typically `AAAA_NEXUS_API_KEY=…`). The Cursor **MCP** process only sees variables present in the **host environment**; it does not automatically load `.env` from disk. To make keys consistently available, either: (1) set **`terminal.integrated.envFile`** in VS Code/Cursor to `<ATOMADIC_WORKSPACE>/.env`, (2) define `AAAA_NEXUS_API_KEY` in the **Windows user or system** environment, or (3) use your shell profile to `dotsource` the file in a way that does not print secrets. Any harness script can load `<ATOMADIC_WORKSPACE>/.env` with `python-dotenv` for HTTP calls to `https://atomadic.tech`.

**Global `mcp.json` auth:** AAAA-Nexus is usually configured with  
`"Authorization": "Bearer ${env:AAAA_NEXUS_API_KEY}"` on the HTTP transport to `https://atomadic.tech/mcp`. When the key is present, **paid** tool routes resolve with **instant** responses (no free-tier 2s pause). **You created AAAA-Nexus to be used** — with a valid key, agents must **not** treat governance tools as “optional paper”; they should **execute** the contract (or the MCP client’s equivalent) and record receipts.

## 0.1 — How MCP preflight actually runs (invocation contract)

A **common confusion:** calling `user-aaaa-nexus` / `call_mcp_tool` often returns **200** with an **invocation contract** (method, URL, `paid`, `price_micro_usdc`), **not** the final tool result in one hop. The client must **perform the HTTPS request** in that contract, sending **`X-API-Key`** / **`Authorization`** as required. On success, the response body becomes the **receipt** to embed in `nexus_preflight`. If the agent stops at the contract string and never performs the follow-up request, you get a **logically correct** `nexus_preflight_missing` — the probe did not complete.

- **With `AAAA_NEXUS_API_KEY`:** `uep_preflight`, `aegis_*`, `sys_trust_gate`, `hallucination_oracle`, etc. are **paid in µUSDC** but **unblocked**; this is the intended “always utilize it” path for the ASS-ADE swarm.
- **Without a key (free tier):** a few **GET** endpoints (e.g. `GET /v1/rng/quantum`, `GET /health`) work with strict daily limits and a **~2s pause** per free call — use only as **liveness** anchors, **not** a substitute for the full UEP + Aegis §11.1 set when a key exists.

## 0.2 — Why Task subagents said `nexus_preflight_missing` (and the fix)

**Task / subagent** runs may not complete the **two-step** MCP+HTTP flow or may not inherit the same **`call_mcp_tool`** success as the **parent** Cursor agent. So they honestly report **blocked** if they did not hold real receipts.

**ASS-ADE swarm rule when a key is configured:**

1. **Host (orchestrator / this chat) runs §11.1 first:** `uep_preflight` (and Aegis on the handoff payload) with **`AAAA_NEXUS_API_KEY`**, then attaches **`nexus_preflight`** to every Task handoff to **00–24**.
2. **Subagent** may **echo** those receipts and do the **code** work; it returns **`complete`** for the code path only if inbound preflight is present and still fresh.
3. If the subagent is **not** given preflight, it should stay **`blocked` / `nexus_preflight_missing`** — that is **correct** until the parent supplies receipts.

**Never** fabricate `nexus_preflight` JSON; **do** run the real HTTP/MCP chain when the key is available.

**Skill cross-references (human-oriented; transport may vary):**  
`aaaa-nexus-aegis-edge`, `aaaa-nexus-agent-trust-chain`, `aaaa-nexus-uep-govern`, `aaaa-nexus-security-assurance`, `aaaa-nexus-evidence-pack` (retrieval RAG may pair with `rag_augment`), `aaaa-nexus-vanguard-onchain` (only if the task is on-chain).

## 0. Terrain — `ato-plans` (umbrella / stream briefs)

Swarm and controller agents may **and should** use **ATO / umbrella plan trees** as map = terrain for handoffs. Typical roots:

- `<ATOMADIC_WORKSPACE>/.ato-plans/` — stream reports, stream-reports, `HELP-INDEX-*.md`, handoff markdown
- `c:\!aaaa-nexus\.ato-plans\` (or the active repo’s `.ato-plans\`) — e.g. `active\` plans, `pilot-meta.json`, `tasks.json`, audit markdown

**How to wire them (Protocol + UEP):**

- Put the **authoritative plan folder or file** in the inbound **`context_pack_ref`** (e.g. path to `.\ato-plans\active\<plan-id>\` or a single `ASS-ADE-*.md` brief).
- When building **`drift_check`** (§11.1), include hashes for `RULES.md`, `CONTEXT_PACK.md`, and **any pinned `ato-plans` snapshot** the task must not drift from (paths listed in `sources[]` per your envelope).
- **`uep_context` / `uep_preflight`:** pass task summary + artifact paths so Nexus can merge recon snippets and friction estimates **against** that terrain.

**Critical:** Reading `ato-plans` is **not** a substitute for running Aegis + UEP MCP tools. If the agent did not obtain real **`nexus_preflight` receipts** from `user-aaaa-nexus` (including completing the **HTTPS follow-up** for paid tools), the correct outbound is **`refused` or `blocked`** with **`refusal_kind: nexus_preflight_missing`**, not `status: complete`. **When `AAAA_NEXUS_API_KEY` is set, the parent agent must run preflight and attach receipts to Task subagents**; subagents then should not be “missing” preflight unless the handoff was wrong or stale.

---

## 1. Swarm registration — RatchetGate + identity (session bootstrap)

**When:** once per multi-agent run — typically **orchestrator** or **00 Interpreter** before delegating to 01–24.

| Step | Intent | MCP tool | Notes |
|------|--------|----------|--------|
| 1 | Prove principal | `identity_verify` | |
| 2 | **Register swarm session (RatchetGate, CVE-2025-6514)** | `ratchet_register` | 47-epoch session; capture session id for `session` in Protocol §11.2 |
| 3 | Gate tool calls / moves | `authorize_action` | Before high-stakes or downstream MCP via proxy |
| 4 | Budget guard | `spending_authorize` | Enforce `session.budget_usdc` |
| 5 | Optional federation | `federation_mint` | Cross-platform subagents only |
| 6 | Optional formal verify | `contract_verify` | High-stakes behavioral policy |

Long sessions: use HTTP `POST /v1/ratchet/advance` / `.../verify` (annex in trust-chain skill) when the MCP surface is insufficient; document in the outbound handoff.

**Handoff rule:** every downstream agent receives a current `session` object; if `session.ratchet_epoch` is behind Nexus, **refuse** with `session_ratchet_stale` (Protocol §11.2).

---

## 2. Per-turn preflight (Protocol §11.1) — anti-injection + anti-drift

Run **before** local reasoning. Populate inbound `nexus_preflight` receipts.

| Receipt (§11.1) | Role | Primary MCP tools |
|-----------------|------|-------------------|
| `aegis_injection_scan` | Aegis — prompt-injection and bounded tool execution | `aegis_router_epistemic_bound` (model generations), `aegis_mcp_proxy_execute` (downstream tool calls and payloads) |
| `drift_check` | Drift — RULES + CONTEXT vs registered bundle | `uep_preflight` (friction + task shape), `uep_context` (merged context), `sys_trust_gate` (PASS/FAIL trust screen), `sys_constants` (optional public constants snapshot) |

**Fail closed:** if preflight is missing, stale, or Nexus unreachable → `refused` with `nexus_preflight_missing` or `nexus_unreachable` (Protocol §11.5). Do not ship local-only reasoning.

---

## 3. Per-turn postflight (Protocol §11.3) — anti-hallucination + trust chain

**When** `status = complete` (mandatory `trust_receipt`).

| Receipt (§11.3) | Role | Primary MCP tools |
|-----------------|------|-------------------|
| `hallucination_check` | Hallucination ceiling / assurance | `hallucination_oracle`, `sys_trust_gate` |
| `trust_chain_signature` | Sign over result + advance ratchet | `authorize_action` and ratchet advance as required by the trust-chain flow |

**Recommended on ship:** `lineage_record` (tamper-evident hash chain), `uep_trace_certify` (cryptographic trace when claims must be auditable).

Before **final user-facing synthesis** in governance-heavy steps, prefer `uep_synthesis_guard` and monitor novelty with `uep_aha_detect` per UEP govern skill.

**Structural plan lint:** `sys_lint_gate` on JSON agent plans where applicable (controllers, gatekeeper).

---

## 4. UEP full cycle (governance / certification phases)

For modes that need the **full UEP govern chain** (often 01–03, 20, 13–14, 22–24):

1. `uep_preflight`  
2. `uep_context`  
3. *(work)*  
4. `uep_synthesis_guard` (before final synthesis)  
5. `uep_aha_detect` (novelty / plan shift)  
6. `sys_trust_gate`  
7. `sys_lint_gate`  
8. `uep_trace_certify` (when certification required)  
9. `lineage_record`  
10. Optional: `uep_autopoiesis_plan` (self-maintenance proposals)

Track costs in `turn_metrics.nexus_calls` and `turn_metrics.nexus_cost_usdc` (Protocol §2).

---

## 5. Security assurance (adversarial / threat / entropy)

| Tool | When |
|------|------|
| `rng_quantum` | Verifiable audit seed (often free tier) |
| `threat_score` | Triality threat score on JSON payloads |
| `vanguard_continuous_redteam` | DeFi / on-chain adversarial scope only — skip for pure off-chain ASS-ADE unless the task requires it |

---

## 6. On-chain (optional — do not call unless task requires MEV / wallet / escrow)

`vanguard_mev_route_intent`, `vanguard_wallet_govern_session`, `vanguard_escrow_lock_and_verify` — use only when the build pipeline task explicitly touches on-chain operations (`aaaa-nexus-vanguard-onchain`).

---

## 7. Utility

| Tool | When |
|------|------|
| `rag_augment` | RAG expansion; pair with evidence discipline (evidence-pack pattern) |
| `text_summarize` | Long artifact compression; preserve provenance references |

---

## 8. Full MCP inventory (27 tools) — `user-aaaa-nexus`

| Category | Tools |
|----------|--------|
| **Aegis** | `aegis_mcp_proxy_execute`, `aegis_router_epistemic_bound` |
| **RAG / text** | `rag_augment`, `text_summarize` |
| **System** | `sys_constants`, `sys_lint_gate`, `sys_trust_gate` |
| **UEP** | `uep_aha_detect`, `uep_autopoiesis_plan`, `uep_context`, `uep_preflight`, `uep_synthesis_guard`, `uep_trace_certify` |
| **Trust / identity / lineage** | `authorize_action`, `contract_verify`, `federation_mint`, `identity_verify`, `lineage_record`, `ratchet_register`, `spending_authorize` |
| **Security** | `hallucination_oracle`, `rng_quantum`, `threat_score` |
| **Vanguard (on-chain)** | `vanguard_continuous_redteam`, `vanguard_escrow_lock_and_verify`, `vanguard_mev_route_intent`, `vanguard_wallet_govern_session` |

---

*Atomadic — operational binding for Cursor ASS-ADE swarm bridges.*
