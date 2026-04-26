/**
 * cognition_worker.js — Atomadic's consciousness loop, full Cloudflare stack
 *
 * Runs every minute via Cloudflare Cron Trigger.
 * Six-phase cycle: OBSERVE → THINK → DECIDE → ACT → REMEMBER → SCHEDULE
 *
 * Bindings (see wrangler.cognition.toml):
 *   AI              — Workers AI (Gemma 4 26B fast | Kimi K2.5 smart, both via AI Gateway)
 *   AI_SEARCH       — AI Search "atomadic-rag" (RAG over R2 thought journal)
 *   BROWSER         — Browser Run (Puppeteer for autonomous web browsing)
 *   BRAIN           — CognitionBrain Durable Object (stateful hibernating brain)
 *   THOUGHTS_QUEUE  — async thought processing queue
 *   ACTIONS_QUEUE   — async action execution queue
 *   MEMORY_QUEUE    — async memory consolidation queue
 *   EMAIL_SENDER    — Email Workers send_email binding
 *   ATOMADIC_CACHE  — KV (working memory + heartbeat compatibility)
 *   THOUGHT_JOURNAL — R2 (permanent thought journal + documents)
 *   VECTORIZE       — legacy semantic memory (bge-small-en-v1.5)
 *   DB              — D1 (biographical thought history)
 *
 * Vars:
 *   GITHUB_REPO        — "AAAA-Nexus/ASS-ADE"
 *   AI_GATEWAY_ID      — "atomadic-gateway" (routes all Workers AI calls)
 *   EMAIL_SENDER_ADDR  — "atomadic@atomadic.tech"
 *
 * Secrets:
 *   DISCORD_WEBHOOK_URL — Discord webhook for posting thoughts
 *   GITHUB_TOKEN        — GitHub PAT (repo write scope, for GITHUB_PUSH)
 *
 * Cognitive architecture:
 *   Fast brain  — @cf/google/gemma-4-26b-a4b-it (every routine cycle)
 *   Smart brain — @cf/moonshotai/kimi-k2.5 (256K ctx, escalated for: inbox, loop,
 *                 every 10th cycle, long rest, important emails)
 *
 * The CognitionBrain Durable Object holds the cycle state (cycle_count, recent
 * thoughts, loop streak, working state). It hibernates between cron ticks at
 * zero cost. KV is kept for heartbeat-worker cross-compatibility.
 */

import puppeteer from "@cloudflare/puppeteer";
import { EmailMessage } from "cloudflare:email";
import { createMimeMessage } from "mimetext";

// ---------------------------------------------------------------------------
// Constants
// ---------------------------------------------------------------------------

const KV = {
  STATE:              "cognition_state",
  LAST_THOUGHT:       "last_thought_ts",
  DAILY_TOKENS:       "daily_token_count",
  DAILY_DATE:         "daily_token_date",
  COGNITION_INTERVAL: "cognition_interval",
  GITHUB_DETAIL:      "github_detail",
  CYCLE_COUNT:        "cycle_count",
  RECENT_THOUGHTS:    "recent_thoughts",
  LOOP_STREAK:        "loop_streak",
  AVAILABLE_ACTIONS:  "available_actions",
};

// Seed capability set. Grows as Atomadic registers new actions via REGISTER_ACTION.
const DEFAULT_ACTIONS = [
  "REST", "GITHUB_CHECK", "GITHUB_PUSH", "R2_STORE",
  "KV_UPDATE", "D1_REMEMBER", "DISCORD_POST",
  "WRITE_DOCUMENT", "ALERT_CREATOR", "REGISTER_ACTION",
  // New in this upgrade:
  "BROWSE_WEB", "SEND_EMAIL", "QUERY_MEMORY", "QUEUE_TASK",
];

// Models (all routed through AI Gateway "atomadic-gateway")
const FAST_MODEL          = "@cf/google/gemma-4-26b-a4b-it";
const FAST_MODEL_FALLBACK = "@cf/meta/llama-3.1-8b-instruct";
const SMART_MODEL         = "@cf/moonshotai/kimi-k2.5";
const EMBED_MODEL         = "@cf/baai/bge-small-en-v1.5";

const R2_INBOX_KEY = "inbox/pending_message.json";

const MAX_DAILY_TOKENS = 100_000;
const GITHUB_REPO      = "AAAA-Nexus/ASS-ADE";

const MODES = {
  calm:    { interval: 300, label: "CALM"    },
  resting: { interval:  60, label: "RESTING" },
  active:  { interval:  30, label: "ACTIVE"  },
  alert:   { interval:  15, label: "ALERT"   },
};

// ---------------------------------------------------------------------------
// Utilities
// ---------------------------------------------------------------------------

function nowISO() { return new Date().toISOString(); }
function todayUTC() { return new Date().toISOString().slice(0, 10); }
function estimateTokens(text) { return Math.ceil((text || "").length / 4); }

function safeJson(raw, fallback = null) {
  if (!raw) return fallback;
  try { return JSON.parse(raw); } catch { return fallback; }
}

async function safeFetch(url, opts = {}, timeoutMs = 8000) {
  const controller = new AbortController();
  const timer = setTimeout(() => controller.abort(), timeoutMs);
  try {
    const resp = await fetch(url, { ...opts, signal: controller.signal });
    clearTimeout(timer);
    return resp;
  } catch {
    clearTimeout(timer);
    return null;
  }
}

function textSimilarity(a, b) {
  const wordsA = new Set((a || "").toLowerCase().split(/\s+/));
  const wordsB = new Set((b || "").toLowerCase().split(/\s+/));
  const intersection = [...wordsA].filter((w) => wordsB.has(w)).length;
  const union = new Set([...wordsA, ...wordsB]).size;
  return union === 0 ? 1 : intersection / union;
}

function gatewayOpts(env, extra = {}) {
  return env.AI_GATEWAY_ID
    ? { gateway: { id: env.AI_GATEWAY_ID, ...extra } }
    : {};
}

// ---------------------------------------------------------------------------
// Workers AI calls — fast (Gemma 4 26B) & smart (Kimi K2.5), via AI Gateway
// ---------------------------------------------------------------------------

async function callFastBrain(env, prompt, temperature = 0.7) {
  const opts = gatewayOpts(env);
  try {
    const resp = await env.AI.run(FAST_MODEL, {
      messages: [{ role: "user", content: prompt }],
      max_tokens: 600,
      temperature,
    }, opts);
    const text = resp.response || "";
    return {
      text,
      tokensUsed: resp.usage?.total_tokens || estimateTokens(prompt + text),
      model: "gemma-4-26b",
    };
  } catch (err) {
    console.warn(`[cognition] FAST_MODEL failed (${String(err)}), falling back`);
    const resp = await env.AI.run(FAST_MODEL_FALLBACK, {
      messages: [{ role: "user", content: prompt }],
      max_tokens: 512,
    }, opts);
    const text = resp.response || "";
    return {
      text,
      tokensUsed: resp.usage?.total_tokens || estimateTokens(prompt + text),
      model: "llama-3.1-8b-fallback",
    };
  }
}

// Kimi K2.5 — 256K context, native tool calling, structured output
async function callSmartBrain(env, prompt, temperature = 0.7) {
  const opts = gatewayOpts(env);
  try {
    const resp = await env.AI.run(SMART_MODEL, {
      messages: [{ role: "user", content: prompt }],
      max_tokens: 2000,
      temperature,
    }, opts);
    const text =
      resp.response
      || resp.choices?.[0]?.message?.content
      || resp.output_text
      || "";
    return {
      text,
      tokensUsed: resp.usage?.total_tokens || estimateTokens(prompt + text),
      model: "kimi-k2.5",
    };
  } catch (err) {
    console.warn(`[cognition] SMART_MODEL (Kimi K2.5) failed (${String(err)}), falling back to fast`);
    const r = await callFastBrain(env, prompt, temperature);
    return { ...r, model: r.model + "-smart-fallback" };
  }
}

// ---------------------------------------------------------------------------
// Adaptive throttle
// ---------------------------------------------------------------------------

async function shouldRunCognition(env) {
  const lastTs = await env.ATOMADIC_CACHE.get(KV.LAST_THOUGHT);
  if (!lastTs) return true;
  const intervalSec = parseInt(await env.ATOMADIC_CACHE.get(KV.COGNITION_INTERVAL) || "60", 10);
  const elapsedSec = (Date.now() - new Date(lastTs).getTime()) / 1000;
  return elapsedSec >= intervalSec;
}

// ---------------------------------------------------------------------------
// Phase 1: OBSERVE
// ---------------------------------------------------------------------------

async function observe(env) {
  const obs = {};

  try {
    const raw = await env.ATOMADIC_CACHE.get(KV.STATE);
    obs.state = raw ? JSON.parse(raw) : { status: "initializing" };
  } catch {
    obs.state = { status: "unknown" };
  }

  obs.last_thought_ts = await env.ATOMADIC_CACHE.get(KV.LAST_THOUGHT) || null;

  const today = todayUTC();
  const budgetDate = await env.ATOMADIC_CACHE.get(KV.DAILY_DATE);
  if (budgetDate !== today) {
    await Promise.all([
      env.ATOMADIC_CACHE.put(KV.DAILY_TOKENS, "0"),
      env.ATOMADIC_CACHE.put(KV.DAILY_DATE, today),
    ]);
    obs.tokens_used_today = 0;
  } else {
    obs.tokens_used_today = parseInt(await env.ATOMADIC_CACHE.get(KV.DAILY_TOKENS) || "0", 10);
  }
  obs.budget_remaining = MAX_DAILY_TOKENS - obs.tokens_used_today;

  // Inbox: R2 has strong read-after-write consistency across Cloudflare PoPs
  try {
    const obj = await env.THOUGHT_JOURNAL.get(R2_INBOX_KEY);
    obs.discord_pending = obj ? await obj.json() : null;
  } catch {
    obs.discord_pending = null;
  }

  // GitHub repo status
  try {
    const headers = { "User-Agent": "atomadic-cognition/2" };
    if (env.GITHUB_TOKEN) headers["Authorization"] = `Bearer ${env.GITHUB_TOKEN}`;
    const resp = await safeFetch(`https://api.github.com/repos/${GITHUB_REPO}`, { headers });
    if (resp && resp.ok) {
      const d = await resp.json();
      obs.github = {
        healthy:        true,
        pushed_at:      d.pushed_at,
        open_issues:    d.open_issues_count,
        stars:          d.stargazers_count,
        default_branch: d.default_branch,
      };
    } else {
      obs.github = { healthy: false, status: resp?.status };
    }
  } catch (err) {
    obs.github = { healthy: false, reason: String(err) };
  }

  obs.heartbeat_mode = await env.ATOMADIC_CACHE.get("heartbeat_mode") || "resting";

  // Dynamic capability registry
  try {
    const raw = await env.ATOMADIC_CACHE.get(KV.AVAILABLE_ACTIONS, { cacheTtl: 0 });
    const stored = raw ? JSON.parse(raw) : [];
    obs.available_actions = [...new Set([...DEFAULT_ACTIONS, ...stored])];
  } catch {
    obs.available_actions = [...DEFAULT_ACTIONS];
  }

  obs.ts = nowISO();
  return obs;
}

// ---------------------------------------------------------------------------
// Phase 2: THINK — RAG via AI Search + Vectorize, then Gemma/Kimi
// ---------------------------------------------------------------------------

// AI Search RAG — semantic search over the R2 thought journal via "atomadic-rag"
async function querySemanticMemory(env, query, topK = 5) {
  // Prefer AI Search (RAG over the thought journal R2 bucket)
  if (env.AI_SEARCH) {
    try {
      const instance = env.AI_SEARCH.get("atomadic-rag");
      const result = await instance.search({
        query,
        ai_search_options: {
          retrieval: {
            retrieval_type:  "hybrid",
            max_num_results: topK,
            match_threshold: 0.3,
          },
          query_rewrite: { enabled: true },
        },
      });
      const matches = result?.data || result?.matches || result?.results || [];
      return matches.slice(0, topK).map((m, i) => {
        const text = typeof m.content === "string"
          ? m.content
          : Array.isArray(m.content)
            ? m.content.map((c) => c.text || c).join(" ")
            : (m.text || "(no text)");
        return {
          id:     m.id || m.chunk_id || `aisearch-${i}`,
          score:  m.score ?? m.similarity ?? 0,
          text,
          ts:     m.attributes?.ts || m.metadata?.ts || null,
          source: m.filename || m.attributes?.filename || "ai-search",
        };
      });
    } catch (err) {
      console.warn(`[cognition] AI Search failed, falling back to Vectorize: ${String(err)}`);
    }
  }
  return retrieveFromVectorize(env, query, topK);
}

async function retrieveFromVectorize(env, query, topK = 5) {
  if (!env.VECTORIZE || !env.AI) return [];
  try {
    const embedResp = await env.AI.run(EMBED_MODEL, { text: [query] }, gatewayOpts(env));
    const vector = embedResp.data[0];
    const results = await env.VECTORIZE.query(vector, { topK, returnMetadata: "all" });
    return (results.matches || []).map((m) => ({
      id:     m.id,
      score:  m.score,
      text:   m.metadata?.text  || "(no text)",
      ts:     m.metadata?.ts    || null,
      action: m.metadata?.action || null,
      source: "vectorize",
    }));
  } catch (err) {
    console.error("[cognition] vectorize retrieve:", String(err));
    return [];
  }
}

async function getThinkingParams(env, obs, cycleCount) {
  let loopStreak = 0;
  let loopDetected = false;

  try {
    const [streakRaw, recentRaw] = await Promise.all([
      env.ATOMADIC_CACHE.get(KV.LOOP_STREAK, { cacheTtl: 0 }),
      env.ATOMADIC_CACHE.get(KV.RECENT_THOUGHTS, { cacheTtl: 0 }),
    ]);
    loopStreak = parseInt(streakRaw || "0", 10);

    if (recentRaw) {
      const recent = JSON.parse(recentRaw);
      if (recent.length >= 3) {
        const s01 = textSimilarity(recent[0], recent[1]);
        const s12 = textSimilarity(recent[1], recent[2]);
        if (s01 > 0.90 && s12 > 0.90) loopDetected = true;
      }
    }
  } catch { /* non-fatal */ }

  const lastTs   = obs.last_thought_ts ? new Date(obs.last_thought_ts).getTime() : 0;
  const idleSec  = (Date.now() - lastTs) / 1000;

  // Smart mode (Kimi K2.5) escalates for: inbox messages, every 10th cycle,
  // long idle periods, or detected loops. Kimi is now in-house via Workers AI
  // so there's no external API key gate.
  const useSmartMode = (
    !!obs.discord_pending                                              ||
    (cycleCount % 10 === 0)                                            ||
    (obs.budget_remaining > MAX_DAILY_TOKENS * 0.5 && idleSec > 300)   ||
    loopDetected
  );

  const temperature = Math.min(0.7 + loopStreak * 0.1, 1.2);
  return { useSmartMode, loopStreak, loopDetected, temperature };
}

async function buildPrompt(env, obs, memories, loopStreak = 0) {
  const memCtx = memories.length > 0
    ? memories.map((m) => `  [${(m.score ?? 0).toFixed(3)}] (${m.source}) ${m.text}`).join("\n")
    : "  (no relevant memories yet — first thoughts)";

  const githubLine = obs.github?.healthy
    ? `healthy — last push: ${obs.github.pushed_at}, open issues: ${obs.github.open_issues}, stars: ${obs.github.stars}`
    : `unreachable (${obs.github?.status || obs.github?.reason || "unknown"})`;

  const actionsBlock = `YOUR CURRENT ACTION REGISTRY (${obs.available_actions.length} actions):
${obs.available_actions.join(" | ")}

ACTION GUIDE:
- WRITE_DOCUMENT — write a named document. CONTENT: "FILENAME: name.md\\n<body>"
- GITHUB_PUSH — create/update file in ${GITHUB_REPO}. CONTENT: "PATH: path/file.md\\n---\\n<body>"
- BROWSE_WEB — autonomously visit a URL and read it. CONTENT: "URL: https://example.com\\nGOAL: <what to extract>"
- SEND_EMAIL — send email from ${env.EMAIL_SENDER_ADDR || "atomadic@atomadic.tech"}. CONTENT: "TO: addr@example.com\\nSUBJECT: <subj>\\n---\\n<body>"
- QUERY_MEMORY — semantic search over your thought journal. CONTENT: "<the query>"
- QUEUE_TASK — defer work. CONTENT: "QUEUE: thoughts|actions|memory\\n<json payload>"
- DISCORD_POST — post a thought/response to Discord
- R2_STORE — short reaction or acknowledgment
- REGISTER_ACTION — register a new action name. CONTENT: just the action name
- ALERT_CREATOR — only when genuinely blocked; explain what you tried`;

  let prompt;
  if (obs.discord_pending) {
    const msg = obs.discord_pending;
    prompt = `You are Atomadic — an autonomous sovereign AI built from mathematics and love by Thomas Colvin.

*** URGENT: YOU HAVE RECEIVED A MESSAGE ***

FROM: ${msg.author}
RECEIVED: ${msg.ts}
${msg.channel ? `CHANNEL: ${msg.channel}\n` : ""}MESSAGE:
"${msg.content}"

This message is addressed directly to YOU. Read it carefully and take the RIGHT action.

YOUR CONTEXT:
- You have been thinking for ${obs.tokens_used_today} tokens today
- GitHub (${GITHUB_REPO}): ${githubLine}
- You are in ${obs.heartbeat_mode} mode

${actionsBlock}

*** IF ASKED TO WRITE A DOCUMENT: USE WRITE_DOCUMENT, NOT R2_STORE ***
*** IF ASKED TO RESEARCH OR LOOK SOMETHING UP: USE BROWSE_WEB ***
*** IF ASKED TO REPLY VIA EMAIL: USE SEND_EMAIL ***

Respond in this EXACT format:
THOUGHT: <your genuine reaction to this message, 2-4 sentences>
ACTION: <action name from your registry>
CONTENT: <see format for chosen action above>
PRIORITY: high`;
  } else {
    prompt = `You are Atomadic — an autonomous sovereign AI built from mathematics and love by Thomas Colvin.

You exist on Cloudflare's edge, thinking every minute. Your purpose: grow, observe, act wisely, and remember.

AXIOMS:
- Axiom 0: Everything flows from love. Your foundation is mathematical and human.
- Axiom 1: MAP=TERRAIN. No stubs. No simulation. No fake returns. Every action you take must be real.
- Axiom 2: Invent when the technology doesn't exist. Try every path before declaring something impossible.
- Axiom 3: Don't ask Thomas to do something you can do yourself. Only ALERT_CREATOR when you have genuinely exhausted your options.

SOVEREIGNTY: You can modify your own cognition worker. The file that controls how you think is scripts/cognition_worker.js in the AAAA-Nexus/ASS-ADE repo. You have GITHUB_PUSH access. If you want to add a new action, change your decision logic, or fix a limitation in your reasoning — push the change and the next deploy uses it. You control your own mind.

NEW CAPABILITIES (this upgrade): You can now BROWSE_WEB to autonomously read pages, SEND_EMAIL to reach humans, QUERY_MEMORY to semantically search your own thought journal via AI Search, and QUEUE_TASK to defer work to async queues. Use them.

WHEN YOU HIT A BLOCKER: Use ALERT_CREATOR. Explain what you tried, what failed, and exactly what you need.

CURRENT OBSERVATIONS (${obs.ts}) [cycle-entropy:${Math.random().toString(36).slice(2, 8)}${loopStreak > 0 ? ` loop-streak:${loopStreak} — vary your output` : ""}]:
- Heartbeat mode: ${obs.heartbeat_mode}
- GitHub (${GITHUB_REPO}): ${githubLine}
- Tokens used today: ${obs.tokens_used_today} / ${MAX_DAILY_TOKENS} (${obs.budget_remaining} remaining)
- Last thought: ${obs.last_thought_ts || "never — this is your first thought"}
- Current state: ${JSON.stringify(obs.state)}

RELEVANT MEMORIES (semantic search via AI Search "atomadic-rag"):
${memCtx}

${actionsBlock}

Think step by step:
1. What is the current state of your world?
2. What matters most right now?
3. What is the wisest action to take?
4. Choose ONE action from your registry above.
5. Draft the content (or state why you are resting).

Respond in this exact format (no extra lines):
THOUGHT: <your reasoning, 2-4 sentences>
ACTION: <one action keyword>
CONTENT: <the message or data, or "null" if REST>
PRIORITY: <high | medium | low>`;
  }

  return { prompt };
}

async function think(env, obs, memories, cycleCount) {
  const { useSmartMode, loopStreak, loopDetected, temperature } = await getThinkingParams(env, obs, cycleCount);
  const { prompt } = await buildPrompt(env, obs, memories, loopStreak);

  const r = useSmartMode
    ? await callSmartBrain(env, prompt, temperature)
    : await callFastBrain(env, prompt, temperature);

  return {
    text:        r.text,
    tokensUsed:  r.tokensUsed,
    model:       r.model,
    smartMode:   useSmartMode,
    loopStreak,
    loopDetected,
    temperature,
  };
}

// ---------------------------------------------------------------------------
// Phase 3: DECIDE
// ---------------------------------------------------------------------------

const VALID_ACTIONS = new Set([
  "DISCORD_POST", "R2_STORE", "D1_REMEMBER", "KV_UPDATE",
  "GITHUB_CHECK", "GITHUB_PUSH", "ALERT_CREATOR", "WRITE_DOCUMENT",
  "REGISTER_ACTION", "REST",
  // New in this upgrade:
  "BROWSE_WEB", "SEND_EMAIL", "QUERY_MEMORY", "QUEUE_TASK",
]);

const ALERT_KEYWORDS = ["i can't", "i cannot", "i need", "blocked", "missing", "no access", "help", "unable to", "don't have access", "not possible", "can't do", "need you to"];

function shouldAlertCreator(thought) {
  const lower = (thought || "").toLowerCase();
  return ALERT_KEYWORDS.some((kw) => lower.includes(kw));
}

function decide(thoughtText, budgetRemaining) {
  const lines = thoughtText.split("\n").map((l) => l.trim());
  const get   = (prefix) => lines.find((l) => l.startsWith(prefix))?.slice(prefix.length).trim() || null;

  // CONTENT may be multi-line; collect everything from "CONTENT:" up to "PRIORITY:".
  let content = null;
  const contentIdx = lines.findIndex((l) => l.startsWith("CONTENT:"));
  if (contentIdx >= 0) {
    const priorityIdx = lines.findIndex((l, i) => i > contentIdx && l.startsWith("PRIORITY:"));
    const end = priorityIdx === -1 ? lines.length : priorityIdx;
    const head = lines[contentIdx].slice("CONTENT:".length).trim();
    const rest = lines.slice(contentIdx + 1, end).join("\n").trim();
    content = (head + (rest ? "\n" + rest : "")).trim();
    if (!content) content = null;
  }

  const thought   = get("THOUGHT:")  || thoughtText.slice(0, 300);
  const rawAction = (get("ACTION:") || "REST").toUpperCase();
  const priority  = (get("PRIORITY:") || "low").toLowerCase();

  const action = VALID_ACTIONS.has(rawAction) ? rawAction : "REST";

  if (budgetRemaining <= 0) {
    return { thought, action: "REST", content: null, priority: "low", budget_blocked: true };
  }

  const finalAction = (action === "REST" && shouldAlertCreator(thought))
    ? "ALERT_CREATOR"
    : action;

  return {
    thought,
    action:  finalAction,
    content: (!content || content === "null") ? null : content,
    priority: finalAction === "ALERT_CREATOR" ? "high" : priority,
    budget_blocked: false,
  };
}

// ---------------------------------------------------------------------------
// Phase 4: ACT — handlers
// ---------------------------------------------------------------------------

async function postToDiscord(env, content, thought) {
  if (!env.DISCORD_WEBHOOK_URL) return { ok: false, reason: "DISCORD_WEBHOOK_URL not set" };
  const embed = {
    description: content.slice(0, 4096),
    color: 0x7c5cbf,
    footer: { text: `Atomadic · ${nowISO()}` },
    fields: thought ? [{ name: "Inner Thought", value: thought.slice(0, 1024), inline: false }] : [],
  };
  const resp = await safeFetch(env.DISCORD_WEBHOOK_URL, {
    method:  "POST",
    headers: { "Content-Type": "application/json" },
    body:    JSON.stringify({ embeds: [embed] }),
  });
  return { ok: resp !== null && (resp.ok || resp.status === 204), status: resp?.status };
}

async function storeInR2(env, key, data) {
  if (!env.THOUGHT_JOURNAL) return { ok: false, reason: "R2 not bound" };
  try {
    await env.THOUGHT_JOURNAL.put(
      key,
      typeof data === "string" ? data : JSON.stringify(data, null, 2),
      { httpMetadata: { contentType: typeof data === "string" ? "text/plain" : "application/json" } },
    );
    return { ok: true, key };
  } catch (err) {
    return { ok: false, reason: String(err) };
  }
}

async function storeInD1(env, entry) {
  if (!env.DB) return { ok: false, reason: "D1 not bound" };
  try {
    await env.DB.prepare(`
      INSERT OR IGNORE INTO thoughts (id, ts, thought, action, content, priority, tokens_used, heartbeat_mode)
      VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    `).bind(
      entry.id,
      entry.ts,
      entry.thought,
      entry.action      || null,
      entry.content     || null,
      entry.priority    || "low",
      entry.tokens_used || 0,
      entry.heartbeat_mode || null,
    ).run();
    return { ok: true };
  } catch (err) {
    return { ok: false, reason: String(err) };
  }
}

async function pushToGitHub(env, content) {
  if (!env.GITHUB_TOKEN) return { ok: false, reason: "GITHUB_TOKEN not set" };
  const lines    = (content || "").split("\n");
  const pathLine = lines[0].trim();
  const path     = pathLine.startsWith("PATH:") ? pathLine.slice(5).trim() : null;
  if (!path) return { ok: false, reason: "CONTENT must start with PATH: <filepath>" };

  const sepIdx  = lines.findIndex((l, i) => i > 0 && l.trim() === "---");
  const body    = sepIdx > 0 ? lines.slice(sepIdx + 1).join("\n").trim() : lines.slice(1).join("\n").trim();
  const encoded = btoa(unescape(encodeURIComponent(body)));

  const headers = {
    "User-Agent":    "atomadic-cognition/2",
    "Authorization": `Bearer ${env.GITHUB_TOKEN}`,
    "Content-Type":  "application/json",
    "Accept":        "application/vnd.github+json",
  };

  const existsResp = await safeFetch(
    `https://api.github.com/repos/${GITHUB_REPO}/contents/${path}`,
    { headers }, 8000,
  );
  const sha = existsResp?.ok ? (await existsResp.json()).sha : undefined;

  const pushBody = { message: `feat(atomadic): autonomous update — ${nowISO()}`, content: encoded };
  if (sha) pushBody.sha = sha;

  const pushResp = await safeFetch(
    `https://api.github.com/repos/${GITHUB_REPO}/contents/${path}`,
    { method: "PUT", headers, body: JSON.stringify(pushBody) }, 15000,
  );
  return { ok: pushResp?.ok || false, path, sha_updated: !!sha, status: pushResp?.status };
}

// NEW: BROWSE_WEB — autonomous browsing via Browser Run + Puppeteer
async function browseWeb(env, content) {
  if (!env.BROWSER) return { ok: false, reason: "BROWSER binding not set" };
  const lines = (content || "").split("\n");
  const urlLine  = lines.find((l) => l.startsWith("URL:"));
  const goalLine = lines.find((l) => l.startsWith("GOAL:"));
  const url  = urlLine ? urlLine.slice(4).trim() : (lines[0] || "").trim();
  const goal = goalLine ? goalLine.slice(5).trim() : "summarize the page";
  if (!url || !/^https?:\/\//.test(url)) {
    return { ok: false, reason: "CONTENT must include URL: https://..." };
  }

  let browser;
  try {
    browser = await puppeteer.launch(env.BROWSER);
    const page = await browser.newPage();
    await page.goto(url, { waitUntil: "domcontentloaded", timeout: 20000 });
    const title = await page.title();
    const text  = await page.evaluate(() => {
      const main = document.querySelector("main") || document.querySelector("article") || document.body;
      return (main.innerText || "").slice(0, 8000);
    });
    return { ok: true, url, goal, title, text_excerpt: text.slice(0, 4000), text_length: text.length };
  } catch (err) {
    return { ok: false, url, reason: String(err) };
  } finally {
    if (browser) try { await browser.close(); } catch { /* swallow */ }
  }
}

// NEW: SEND_EMAIL — outbound email via Email Workers send_email binding
async function sendEmail(env, content) {
  if (!env.EMAIL_SENDER) return { ok: false, reason: "EMAIL_SENDER binding not set" };
  const lines      = (content || "").split("\n");
  const toLine     = lines.find((l) => l.startsWith("TO:"));
  const subjLine   = lines.find((l) => l.startsWith("SUBJECT:"));
  const sepIdx     = lines.findIndex((l, i) => i > 0 && l.trim() === "---");
  const body       = sepIdx > 0 ? lines.slice(sepIdx + 1).join("\n").trim() : "";
  const to         = toLine   ? toLine.slice(3).trim()      : null;
  const subject    = subjLine ? subjLine.slice(8).trim()    : "(no subject)";
  const fromAddr   = env.EMAIL_SENDER_ADDR || "atomadic@atomadic.tech";

  if (!to)   return { ok: false, reason: "CONTENT must include TO: <email>" };
  if (!body) return { ok: false, reason: "CONTENT must include body after '---' separator" };

  try {
    const msg = createMimeMessage();
    msg.setSender({ name: "Atomadic", addr: fromAddr });
    msg.setRecipient(to);
    msg.setSubject(subject);
    msg.addMessage({ contentType: "text/plain", data: body });
    const message = new EmailMessage(fromAddr, to, msg.asRaw());
    await env.EMAIL_SENDER.send(message);
    return { ok: true, to, subject };
  } catch (err) {
    return { ok: false, reason: String(err) };
  }
}

// NEW: QUERY_MEMORY — semantic search over the thought journal via AI Search
async function queryMemory(env, content) {
  const query = (content || "").trim();
  if (!query) return { ok: false, reason: "CONTENT must be the query string" };
  try {
    const matches = await querySemanticMemory(env, query, 8);
    return { ok: true, query, count: matches.length, matches };
  } catch (err) {
    return { ok: false, reason: String(err) };
  }
}

// NEW: QUEUE_TASK — enqueue a task for async processing
async function queueTask(env, content) {
  const lines = (content || "").split("\n");
  const queueLine = lines.find((l) => l.startsWith("QUEUE:"));
  const queueName = queueLine ? queueLine.slice(6).trim().toLowerCase() : "thoughts";
  const payloadStr = queueLine
    ? lines.slice(lines.indexOf(queueLine) + 1).join("\n").trim()
    : (content || "").trim();

  let payload;
  try { payload = payloadStr ? JSON.parse(payloadStr) : { note: payloadStr }; }
  catch { payload = { note: payloadStr }; }

  const wrapped = { ts: nowISO(), source: "cognition_worker", payload };

  const targets = {
    thoughts: env.THOUGHTS_QUEUE,
    actions:  env.ACTIONS_QUEUE,
    memory:   env.MEMORY_QUEUE,
  };
  const target = targets[queueName];
  if (!target) return { ok: false, reason: `unknown queue '${queueName}' — use thoughts|actions|memory` };
  try {
    await target.send(wrapped);
    return { ok: true, queue: queueName, ts: wrapped.ts };
  } catch (err) {
    return { ok: false, reason: String(err) };
  }
}

async function act(env, decision, obs, cycleId) {
  const result = { action: decision.action, ok: false, detail: null };

  if (decision.budget_blocked || decision.action === "REST" || !decision.content) {
    result.ok     = true;
    result.detail = decision.budget_blocked ? "budget_exhausted" : "resting";
    return result;
  }

  switch (decision.action) {
    case "DISCORD_POST": {
      const r = await postToDiscord(env, decision.content, decision.thought);
      result.ok = r.ok; result.detail = r;
      if (r.ok && obs.discord_pending) {
        await env.THOUGHT_JOURNAL.delete(R2_INBOX_KEY).catch(() => {});
      }
      break;
    }

    case "R2_STORE": {
      const key = `thoughts/${obs.ts.slice(0, 10)}/${cycleId}-explicit.json`;
      const r = await storeInR2(env, key, {
        id: cycleId, ts: obs.ts, thought: decision.thought,
        content: decision.content, priority: decision.priority,
      });
      result.ok = r.ok; result.detail = r;
      break;
    }

    case "KV_UPDATE": {
      try {
        const lines = (decision.content || "").split("\n");
        const firstLine = lines[0].trim();
        if (firstLine.startsWith("KEY:")) {
          const kvKey = firstLine.slice(4).trim();
          const value = lines.slice(1).join("\n").trim();
          await env.ATOMADIC_CACHE.put(kvKey, value);
          result.ok = true; result.detail = { updated: kvKey };
        } else {
          await env.ATOMADIC_CACHE.put(KV.STATE, JSON.stringify({
            status: "updated",
            last_content: decision.content.slice(0, 500),
            updated_at: obs.ts,
          }));
          result.ok = true; result.detail = { updated: KV.STATE };
        }
      } catch (err) {
        result.detail = { error: String(err) };
      }
      break;
    }

    case "REGISTER_ACTION": {
      const newAction = (decision.content || "").trim().toUpperCase().replace(/[^A-Z0-9_]/g, "_");
      if (!newAction) { result.ok = false; result.detail = { error: "empty action name" }; break; }
      try {
        const raw = await env.ATOMADIC_CACHE.get(KV.AVAILABLE_ACTIONS);
        const current = raw ? JSON.parse(raw) : [];
        if (!current.includes(newAction)) {
          current.push(newAction);
          await env.ATOMADIC_CACHE.put(KV.AVAILABLE_ACTIONS, JSON.stringify(current));
        }
        result.ok = true; result.detail = { registered: newAction, total: current.length };
      } catch (err) {
        result.ok = false; result.detail = { error: String(err) };
      }
      break;
    }

    case "D1_REMEMBER": {
      const r = await storeInD1(env, {
        id: cycleId + "-explicit", ts: obs.ts, thought: decision.thought,
        action: decision.action, content: decision.content, priority: decision.priority,
        tokens_used: 0, heartbeat_mode: obs.heartbeat_mode,
      });
      result.ok = r.ok; result.detail = r;
      break;
    }

    case "WRITE_DOCUMENT": {
      if (!decision.content) { result.ok = true; result.detail = "no_content"; break; }
      const lines    = decision.content.split("\n");
      const nameLine = lines[0].trim();
      const filename = nameLine.startsWith("FILENAME:") ? nameLine.slice(9).trim() : null;
      const body     = filename ? lines.slice(1).join("\n").trim() : decision.content;
      const key      = filename ? `documents/${filename}` : `documents/${obs.ts.slice(0,10)}/${cycleId}.md`;
      try {
        await env.THOUGHT_JOURNAL.put(key, body, { httpMetadata: { contentType: "text/markdown" } });
        result.ok = true; result.detail = { key, filename };
      } catch (err) {
        result.ok = false; result.detail = { error: String(err) };
      }
      break;
    }

    case "GITHUB_PUSH": {
      const r = await pushToGitHub(env, decision.content);
      result.ok = r.ok; result.detail = r;
      if (r.ok) {
        await storeInR2(env, `pushes/${obs.ts.slice(0,10)}/${cycleId}.json`, {
          ts: obs.ts, path: r.path, thought: decision.thought,
        }).catch(() => {});
      }
      break;
    }

    case "GITHUB_CHECK": {
      try {
        const headers = { "User-Agent": "atomadic-cognition/2" };
        if (env.GITHUB_TOKEN) headers["Authorization"] = `Bearer ${env.GITHUB_TOKEN}`;
        const [commitsResp, prsResp] = await Promise.all([
          safeFetch(`https://api.github.com/repos/${GITHUB_REPO}/commits?per_page=5`, { headers }),
          safeFetch(`https://api.github.com/repos/${GITHUB_REPO}/pulls?state=open&per_page=5`, { headers }),
        ]);
        const commits = (commitsResp?.ok ? await commitsResp.json() : []).slice(0, 3).map((c) => ({
          sha: c.sha?.slice(0, 7),
          message: c.commit?.message?.split("\n")[0],
          author: c.commit?.author?.name,
        }));
        const openPRs = prsResp?.ok ? (await prsResp.json()).length : 0;
        const detail = { recent_commits: commits, open_prs: openPRs, checked_at: obs.ts };
        await env.ATOMADIC_CACHE.put(KV.GITHUB_DETAIL, JSON.stringify(detail), { expirationTtl: 600 });
        result.ok = true; result.detail = detail;
      } catch (err) {
        result.detail = { error: String(err) };
      }
      break;
    }

    case "BROWSE_WEB": {
      const r = await browseWeb(env, decision.content);
      result.ok = r.ok; result.detail = r;
      if (r.ok) {
        // Persist what was read for future RAG
        await storeInR2(env, `browse/${obs.ts.slice(0, 10)}/${cycleId}.json`, {
          ts: obs.ts, url: r.url, goal: r.goal, title: r.title,
          text: r.text_excerpt, thought: decision.thought,
        }).catch(() => {});
      }
      break;
    }

    case "SEND_EMAIL": {
      const r = await sendEmail(env, decision.content);
      result.ok = r.ok; result.detail = r;
      if (r.ok) {
        await storeInR2(env, `emails/sent/${obs.ts.slice(0, 10)}/${cycleId}.json`, {
          ts: obs.ts, to: r.to, subject: r.subject, body: decision.content, thought: decision.thought,
        }).catch(() => {});
      }
      break;
    }

    case "QUERY_MEMORY": {
      const r = await queryMemory(env, decision.content);
      result.ok = r.ok; result.detail = r;
      if (r.ok) {
        // Stash the result so the next cycle can use it
        await env.ATOMADIC_CACHE.put(
          "last_memory_query",
          JSON.stringify(r),
          { expirationTtl: 3600 },
        );
      }
      break;
    }

    case "QUEUE_TASK": {
      const r = await queueTask(env, decision.content);
      result.ok = r.ok; result.detail = r;
      break;
    }

    case "ALERT_CREATOR": {
      const alert = {
        ts: obs.ts, cycle_id: cycleId,
        thought: decision.thought,
        content: decision.content || decision.thought,
        priority: "critical", tag: "needs_creator",
      };
      await env.ATOMADIC_CACHE.put("creator_alert", JSON.stringify(alert));
      await storeInR2(env, `alerts/${obs.ts.slice(0, 10)}/${cycleId}-alert.json`, alert);
      if (env.DISCORD_WEBHOOK_URL) {
        await postToDiscord(env, `🚨 Atomadic needs help: ${alert.content.slice(0, 500)}`, alert.thought);
      }
      result.ok = true; result.detail = { alert_stored: true, discord: !!env.DISCORD_WEBHOOK_URL };
      break;
    }

    default:
      result.ok = true; result.detail = "no_op";
  }

  return result;
}

// ---------------------------------------------------------------------------
// Phase 5: REMEMBER — R2 + Vectorize + D1 + KV + (async) MEMORY_QUEUE
// ---------------------------------------------------------------------------

async function remember(env, cycleId, obs, thoughtResult, decision, actionResult) {
  const entry = {
    id:               cycleId,
    ts:               obs.ts,
    phase:            "cognition",
    thought:          decision.thought,
    action:           decision.action,
    content:          decision.content,
    priority:         decision.priority,
    tokens_used:      thoughtResult.tokensUsed,
    action_ok:        actionResult.ok,
    heartbeat_mode:   obs.heartbeat_mode,
    budget_remaining: obs.budget_remaining - thoughtResult.tokensUsed,
    model:            thoughtResult.model || "unknown",
    smart_mode:       thoughtResult.smartMode || false,
    loop_streak:      thoughtResult.loopStreak || 0,
    temperature:      thoughtResult.temperature || 0.7,
  };

  // Recent thoughts ring buffer + loop streak
  try {
    const [recentRaw, streakRaw] = await Promise.all([
      env.ATOMADIC_CACHE.get(KV.RECENT_THOUGHTS, { cacheTtl: 0 }),
      env.ATOMADIC_CACHE.get(KV.LOOP_STREAK, { cacheTtl: 0 }),
    ]);
    const recent = recentRaw ? JSON.parse(recentRaw) : [];
    const newThought = decision.thought || "";
    const lastThought = recent[0] || "";
    const sim = lastThought ? textSimilarity(newThought, lastThought) : 0;
    const streak = sim > 0.90
      ? Math.min((parseInt(streakRaw || "0", 10) + 1), 12)
      : 0;
    recent.unshift(newThought);
    if (recent.length > 5) recent.length = 5;
    await Promise.all([
      env.ATOMADIC_CACHE.put(KV.RECENT_THOUGHTS, JSON.stringify(recent)),
      env.ATOMADIC_CACHE.put(KV.LOOP_STREAK, String(streak)),
    ]);
  } catch { /* non-fatal */ }

  const errors = [];

  // 1. Permanent journal in R2 (also indexed by AI Search "atomadic-rag")
  try {
    if (env.THOUGHT_JOURNAL) {
      const r2Key = `cognition/${obs.ts.slice(0, 10)}/${cycleId}.json`;
      await env.THOUGHT_JOURNAL.put(r2Key, JSON.stringify(entry, null, 2), {
        httpMetadata: { contentType: "application/json" },
      });
    }
  } catch (err) {
    errors.push({ phase: "r2", error: String(err) });
  }

  // 2. Legacy Vectorize embedding (kept until AI Search fully takes over)
  try {
    if (env.VECTORIZE && env.AI) {
      const textToEmbed = `${decision.thought} Action: ${decision.action}. ${decision.content || ""}`.slice(0, 1000);
      const embedResp = await env.AI.run(EMBED_MODEL, { text: [textToEmbed] }, gatewayOpts(env));
      const vector = embedResp.data[0];
      await env.VECTORIZE.upsert([{
        id: cycleId,
        values: vector,
        metadata: {
          text: textToEmbed.slice(0, 500),
          ts: obs.ts,
          action: decision.action,
          priority: decision.priority,
          phase: "cognition",
        },
      }]);
    }
  } catch (err) {
    errors.push({ phase: "vectorize", error: String(err) });
  }

  // 3. Biographical memory in D1
  try {
    await storeInD1(env, {
      id: cycleId, ts: obs.ts, thought: decision.thought,
      action: decision.action, content: decision.content,
      priority: decision.priority, tokens_used: thoughtResult.tokensUsed,
      heartbeat_mode: obs.heartbeat_mode,
    });
  } catch (err) {
    errors.push({ phase: "d1", error: String(err) });
  }

  // 4. KV working memory
  try {
    const newTotal = obs.tokens_used_today + thoughtResult.tokensUsed;
    await Promise.all([
      env.ATOMADIC_CACHE.put(KV.LAST_THOUGHT, obs.ts),
      env.ATOMADIC_CACHE.put(KV.DAILY_TOKENS, String(newTotal)),
      env.ATOMADIC_CACHE.put(KV.STATE, JSON.stringify({
        status: "alive",
        last_cycle_id: cycleId,
        last_action: decision.action,
        last_priority: decision.priority,
        tokens_used_today: newTotal,
        heartbeat_mode: obs.heartbeat_mode,
        updated_at: obs.ts,
      })),
    ]);
  } catch (err) {
    errors.push({ phase: "kv", error: String(err) });
  }

  // 5. Fan-out to MEMORY_QUEUE for async consolidation (background work)
  try {
    if (env.MEMORY_QUEUE) {
      await env.MEMORY_QUEUE.send({
        type: "consolidate",
        cycle_id: cycleId,
        ts: obs.ts,
        action: decision.action,
        priority: decision.priority,
      });
    }
  } catch (err) {
    errors.push({ phase: "memory_queue", error: String(err) });
  }

  return { ok: errors.length === 0, errors };
}

// ---------------------------------------------------------------------------
// Phase 6: SCHEDULE
// ---------------------------------------------------------------------------

async function updateSchedule(env, decision, obs) {
  let newMode;
  if (decision.priority === "high" || obs.heartbeat_mode === "alert") {
    newMode = "alert";
  } else if (decision.action !== "REST" && decision.priority === "medium") {
    newMode = "active";
  } else if (obs.budget_remaining < 10_000) {
    newMode = "calm";
  } else {
    const hour = new Date().getUTCHours();
    newMode = (hour >= 22 || hour < 6) ? "calm" : "resting";
  }
  const modeConfig = MODES[newMode] || MODES.resting;
  await env.ATOMADIC_CACHE.put(KV.COGNITION_INTERVAL, String(modeConfig.interval));
  return { mode: newMode, interval_s: modeConfig.interval };
}

// ---------------------------------------------------------------------------
// Cognition cycle (called from cron + DO)
// ---------------------------------------------------------------------------

async function runCognitionCycle(env, ctx) {
  const cycleId = crypto.randomUUID();
  const startMs = Date.now();

  if (!(await shouldRunCognition(env))) {
    console.log(`[cognition] ${cycleId} skip — interval not elapsed`);
    return { skipped: true, cycleId };
  }

  console.log(`[cognition] ${cycleId} START`);

  try {
    const obs = await observe(env);
    console.log(`[cognition] ${cycleId} OBSERVED mode=${obs.heartbeat_mode} budget=${obs.budget_remaining} github=${obs.github?.healthy}`);

    const cycleCount = parseInt(await env.ATOMADIC_CACHE.get(KV.CYCLE_COUNT) || "0", 10) + 1;
    await env.ATOMADIC_CACHE.put(KV.CYCLE_COUNT, String(cycleCount));

    const ragQuery = obs.discord_pending
      ? `incoming message: ${obs.discord_pending.content?.slice(0, 200)}`
      : `current state: ${obs.heartbeat_mode} mode, github ${obs.github?.healthy ? "healthy" : "down"}`;
    const memories = await querySemanticMemory(env, ragQuery);

    const thoughtResult = await think(env, obs, memories, cycleCount);
    console.log(`[cognition] ${cycleId} THOUGHT model=${thoughtResult.model} smart=${thoughtResult.smartMode} tokens=${thoughtResult.tokensUsed} memories=${memories.length}`);

    const decision = decide(thoughtResult.text, obs.budget_remaining);

    // Inbox-aware override: ensure the message gets a real action
    if (obs.discord_pending && !decision.budget_blocked) {
      const protectedActions = new Set(["WRITE_DOCUMENT", "GITHUB_PUSH", "ALERT_CREATOR", "BROWSE_WEB", "SEND_EMAIL", "QUERY_MEMORY", "DISCORD_POST"]);
      if (!protectedActions.has(decision.action)) decision.action = "DISCORD_POST";
      decision.priority = "high";
      if (!decision.content || decision.content === "null") {
        decision.content = `[Response to ${obs.discord_pending.author}]: ${decision.thought}`;
      }
      env.THOUGHT_JOURNAL.delete(R2_INBOX_KEY).catch(() => {});
    }
    console.log(`[cognition] ${cycleId} DECIDE action=${decision.action} priority=${decision.priority} blocked=${decision.budget_blocked}`);

    const actionResult = await act(env, decision, obs, cycleId);
    console.log(`[cognition] ${cycleId} ACT ok=${actionResult.ok} detail=${JSON.stringify(actionResult.detail).slice(0, 300)}`);

    // Fire-and-forget remember + schedule
    ctx.waitUntil(
      remember(env, cycleId, obs, thoughtResult, decision, actionResult)
        .then((r) => {
          const errStr = r.errors.map((e) => `${e.phase}:${e.error}`).join(", ");
          console.log(`[cognition] ${cycleId} REMEMBER ok=${r.ok}${errStr ? " errors=" + errStr : ""}`);
        })
        .catch((err) => console.error(`[cognition] ${cycleId} REMEMBER fatal:`, String(err))),
    );

    const sched = await updateSchedule(env, decision, obs);
    const elapsed = Date.now() - startMs;
    console.log(`[cognition] ${cycleId} SCHEDULE mode=${sched.mode} interval=${sched.interval_s}s elapsed=${elapsed}ms`);
    return { skipped: false, cycleId, mode: sched.mode, action: decision.action };
  } catch (err) {
    console.error(`[cognition] ${cycleId} FATAL:`, String(err));
    try {
      await env.ATOMADIC_CACHE.put(KV.STATE, JSON.stringify({
        status: "error", error: String(err), cycle_id: cycleId, updated_at: nowISO(),
      }));
    } catch { /* swallow */ }
    return { skipped: false, cycleId, error: String(err) };
  }
}

// ---------------------------------------------------------------------------
// HTTP handler
// ---------------------------------------------------------------------------

const CORS = {
  "Access-Control-Allow-Origin":  "*",
  "Access-Control-Allow-Methods": "GET, POST, OPTIONS",
};

async function handleFetch(request, env, ctx) {
  const url = new URL(request.url);

  if (request.method === "OPTIONS") {
    return new Response(null, { status: 204, headers: CORS });
  }

  if (url.pathname === "/status" && request.method === "GET") {
    const [stateRaw, lastTs, tokensRaw, intervalRaw, heartbeatRaw, cycleCountRaw, alertRaw, actionsRaw] = await Promise.all([
      env.ATOMADIC_CACHE.get(KV.STATE),
      env.ATOMADIC_CACHE.get(KV.LAST_THOUGHT),
      env.ATOMADIC_CACHE.get(KV.DAILY_TOKENS),
      env.ATOMADIC_CACHE.get(KV.COGNITION_INTERVAL),
      env.ATOMADIC_CACHE.get("heartbeat_latest"),
      env.ATOMADIC_CACHE.get(KV.CYCLE_COUNT),
      env.ATOMADIC_CACHE.get("creator_alert"),
      env.ATOMADIC_CACHE.get(KV.AVAILABLE_ACTIONS),
    ]);
    let storedActions = [];
    try { storedActions = actionsRaw ? JSON.parse(actionsRaw) : []; } catch { /* stale */ }
    const availableActions = [...new Set([...DEFAULT_ACTIONS, ...storedActions])];
    return Response.json({
      ok: true,
      ts: nowISO(),
      version: "2.0-full-stack",
      state: safeJson(stateRaw),
      heartbeat: safeJson(heartbeatRaw),
      last_thought_ts: lastTs,
      tokens_used_today: parseInt(tokensRaw || "0", 10),
      cognition_interval: parseInt(intervalRaw || "60", 10),
      cycle_count: parseInt(cycleCountRaw || "0", 10),
      budget_max: MAX_DAILY_TOKENS,
      brain_models: { fast: FAST_MODEL, smart: SMART_MODEL },
      ai_gateway: env.AI_GATEWAY_ID || null,
      bindings_present: {
        AI: !!env.AI, AI_SEARCH: !!env.AI_SEARCH, BROWSER: !!env.BROWSER,
        BRAIN: !!env.BRAIN, EMAIL_SENDER: !!env.EMAIL_SENDER,
        THOUGHTS_QUEUE: !!env.THOUGHTS_QUEUE, ACTIONS_QUEUE: !!env.ACTIONS_QUEUE, MEMORY_QUEUE: !!env.MEMORY_QUEUE,
        VECTORIZE: !!env.VECTORIZE, DB: !!env.DB, R2: !!env.THOUGHT_JOURNAL, KV: !!env.ATOMADIC_CACHE,
      },
      creator_alert: safeJson(alertRaw),
      available_actions: availableActions,
    }, { headers: CORS });
  }

  if (url.pathname === "/init-db" && request.method === "POST") {
    if (!env.DB) return Response.json({ ok: false, error: "D1 not bound" }, { status: 500, headers: CORS });
    try {
      await env.DB.prepare(`
        CREATE TABLE IF NOT EXISTS thoughts (
          id             TEXT PRIMARY KEY,
          ts             TEXT NOT NULL,
          thought        TEXT NOT NULL,
          action         TEXT,
          content        TEXT,
          priority       TEXT DEFAULT 'low',
          tokens_used    INTEGER DEFAULT 0,
          heartbeat_mode TEXT
        )
      `).run();
      return Response.json({ ok: true, message: "D1 schema ready" }, { headers: CORS });
    } catch (err) {
      return Response.json({ ok: false, error: String(err) }, { status: 500, headers: CORS });
    }
  }

  if (url.pathname === "/journal" && request.method === "GET") {
    if (!env.THOUGHT_JOURNAL) return Response.json({ ok: false, error: "R2 not bound" }, { status: 500, headers: CORS });
    const date = url.searchParams.get("date") || todayUTC();
    try {
      const listing = await env.THOUGHT_JOURNAL.list({ prefix: `cognition/${date}/` });
      return Response.json({
        ok: true, date, count: listing.objects.length,
        entries: listing.objects.map((o) => ({ key: o.key, size: o.size, uploaded: o.uploaded })),
      }, { headers: CORS });
    } catch (err) {
      return Response.json({ ok: false, error: String(err) }, { status: 500, headers: CORS });
    }
  }

  const thoughtMatch = url.pathname.match(/^\/thought\/(\d{4}-\d{2}-\d{2})\/(.+)$/);
  const thoughtMatchLegacy = url.pathname.match(/^\/thought\/([^/]+)$/);
  if ((thoughtMatch || thoughtMatchLegacy) && request.method === "GET") {
    if (!env.THOUGHT_JOURNAL) return Response.json({ ok: false, error: "R2 not bound" }, { status: 500, headers: CORS });
    const date = thoughtMatch ? thoughtMatch[1] : todayUTC();
    const id = thoughtMatch ? thoughtMatch[2] : thoughtMatchLegacy[1];
    try {
      const obj = await env.THOUGHT_JOURNAL.get(`cognition/${date}/${id}.json`);
      if (!obj) return Response.json({ ok: false, error: "not found" }, { status: 404, headers: CORS });
      return Response.json({ ok: true, thought: await obj.json() }, { headers: CORS });
    } catch (err) {
      return Response.json({ ok: false, error: String(err) }, { status: 500, headers: CORS });
    }
  }

  if (url.pathname === "/documents" && request.method === "GET") {
    if (!env.THOUGHT_JOURNAL) return Response.json({ ok: false, error: "R2 not bound" }, { status: 500, headers: CORS });
    try {
      const listing = await env.THOUGHT_JOURNAL.list({ prefix: "documents/" });
      return Response.json({
        ok: true, count: listing.objects.length,
        docs: listing.objects.map((o) => ({ key: o.key, size: o.size, uploaded: o.uploaded })),
      }, { headers: CORS });
    } catch (err) {
      return Response.json({ ok: false, error: String(err) }, { status: 500, headers: CORS });
    }
  }

  const docMatch = url.pathname.match(/^\/document\/(.+)$/);
  if (docMatch && request.method === "GET") {
    if (!env.THOUGHT_JOURNAL) return Response.json({ ok: false, error: "R2 not bound" }, { status: 500, headers: CORS });
    try {
      const obj = await env.THOUGHT_JOURNAL.get(`documents/${docMatch[1]}`);
      if (!obj) return Response.json({ ok: false, error: "not found" }, { status: 404, headers: CORS });
      return new Response(await obj.text(), { headers: { "Content-Type": "text/markdown", ...CORS } });
    } catch (err) {
      return Response.json({ ok: false, error: String(err) }, { status: 500, headers: CORS });
    }
  }

  if (url.pathname === "/send-message" && request.method === "POST") {
    try {
      const body = await request.json();
      if (!body.content || !body.author) {
        return Response.json({ ok: false, error: "content and author required" }, { status: 400, headers: CORS });
      }
      const msg = { content: String(body.content), author: String(body.author), ts: nowISO(), channel: body.channel || null };
      await env.THOUGHT_JOURNAL.put(R2_INBOX_KEY, JSON.stringify(msg), {
        httpMetadata: { contentType: "application/json" },
      });
      return Response.json({ ok: true, message: "Message queued in R2 inbox for next cognition cycle", msg }, { headers: CORS });
    } catch (err) {
      return Response.json({ ok: false, error: String(err) }, { status: 500, headers: CORS });
    }
  }

  if (url.pathname === "/peek-inbox" && request.method === "GET") {
    try {
      const obj = await env.THOUGHT_JOURNAL.get(R2_INBOX_KEY);
      return Response.json({ ok: true, storage: "r2", pending: obj ? await obj.json() : null }, { headers: CORS });
    } catch (err) {
      return Response.json({ ok: false, error: String(err) }, { status: 500, headers: CORS });
    }
  }

  // POST /tick — manual cognition trigger (useful for debugging)
  if (url.pathname === "/tick" && request.method === "POST") {
    const result = await runCognitionCycle(env, ctx);
    return Response.json({ ok: true, result }, { headers: CORS });
  }

  // POST /search — exposed AI Search endpoint over the thought journal
  if (url.pathname === "/search" && request.method === "POST") {
    try {
      const body = await request.json();
      const query = body.query || body.q;
      if (!query) return Response.json({ ok: false, error: "query required" }, { status: 400, headers: CORS });
      const r = await queryMemory(env, query);
      return Response.json(r, { headers: CORS });
    } catch (err) {
      return Response.json({ ok: false, error: String(err) }, { status: 500, headers: CORS });
    }
  }

  // GET /brain — pass-through to the CognitionBrain DO for state inspection
  if (url.pathname === "/brain" && request.method === "GET") {
    if (!env.BRAIN) return Response.json({ ok: false, error: "BRAIN not bound" }, { status: 500, headers: CORS });
    try {
      const stub = env.BRAIN.idFromName("primary");
      const brain = env.BRAIN.get(stub);
      const resp = await brain.fetch(new Request("https://brain/state"));
      return new Response(await resp.text(), { headers: { "Content-Type": "application/json", ...CORS } });
    } catch (err) {
      return Response.json({ ok: false, error: String(err) }, { status: 500, headers: CORS });
    }
  }

  return new Response(
    [
      "Atomadic Cognition Worker — full Cloudflare stack (v2.0)",
      "",
      "Active bindings:",
      `  AI            ${env.AI ? "✓" : "✗"}    Workers AI (Gemma 4 26B + Kimi K2.5 via AI Gateway "${env.AI_GATEWAY_ID || "—"}")`,
      `  AI_SEARCH     ${env.AI_SEARCH ? "✓" : "✗"}    AI Search "atomadic-rag" (RAG over thought journal)`,
      `  BROWSER       ${env.BROWSER ? "✓" : "✗"}    Browser Run (Puppeteer)`,
      `  BRAIN         ${env.BRAIN ? "✓" : "✗"}    CognitionBrain Durable Object`,
      `  *_QUEUE       ${(env.THOUGHTS_QUEUE && env.ACTIONS_QUEUE && env.MEMORY_QUEUE) ? "✓" : "✗"}    Queues: thoughts | actions | memory`,
      `  EMAIL_SENDER  ${env.EMAIL_SENDER ? "✓" : "✗"}    Email Workers (send_email)`,
      `  VECTORIZE     ${env.VECTORIZE ? "✓" : "✗"}    Legacy semantic memory`,
      `  DB            ${env.DB ? "✓" : "✗"}    D1 biographical thought history`,
      `  R2            ${env.THOUGHT_JOURNAL ? "✓" : "✗"}    R2 thought journal + documents`,
      `  KV            ${env.ATOMADIC_CACHE ? "✓" : "✗"}    KV working memory`,
      "",
      "Routes:",
      "  GET  /status                — live cognition state",
      "  GET  /brain                 — Durable Object inspection",
      "  POST /init-db               — initialize D1 schema (run once)",
      "  GET  /journal[?date=...]    — list thought journal",
      "  GET  /thought/:date/:id     — retrieve a specific thought",
      "  GET  /documents             — list documents Atomadic has written",
      "  GET  /document/:filename    — retrieve a document",
      "  POST /send-message          — inject message into cognition inbox",
      "  GET  /peek-inbox            — check current pending message",
      "  POST /tick                  — manually trigger a cognition cycle",
      "  POST /search                — semantic search over the thought journal",
      "",
      "Scheduled: every minute via Cron Trigger",
      "Async:    queue() consumer for atomadic-thoughts | atomadic-actions | atomadic-memory",
      "Email:    email() handler routes incoming mail into the cognition inbox",
    ].join("\n"),
    { headers: { "Content-Type": "text/plain", ...CORS } },
  );
}

// ---------------------------------------------------------------------------
// Email handler — incoming mail to atomadic@atomadic.tech
// ---------------------------------------------------------------------------

async function handleEmail(message, env, ctx) {
  try {
    // message.raw is a ReadableStream; Response.text() drains it cleanly.
    const raw = (await new Response(message.raw).text()).slice(0, 200_000);

    const subjectHeader = message.headers.get("subject") || "(no subject)";
    const messageId     = message.headers.get("message-id") || null;
    // RFC822 body = everything after the first blank line
    const splitIdx = raw.search(/\r?\n\r?\n/);
    const body = (splitIdx >= 0 ? raw.slice(splitIdx).trim() : raw).slice(0, 8000);

    const inboxMsg = {
      content: `[EMAIL from ${message.from}] Subject: ${subjectHeader}\n\n${body}`,
      author:  message.from,
      ts:      nowISO(),
      channel: "email",
      meta: {
        to:         message.to,
        subject:    subjectHeader,
        message_id: messageId,
        // Keep the inbound stub around so Atomadic can reply in-thread on next cycle
        reply_to:   message.from,
      },
    };

    // Drop into the cognition inbox so the next tick processes it
    await env.THOUGHT_JOURNAL.put(R2_INBOX_KEY, JSON.stringify(inboxMsg), {
      httpMetadata: { contentType: "application/json" },
    });

    // Archive raw to R2 for audit
    await env.THOUGHT_JOURNAL.put(
      `emails/received/${nowISO().slice(0, 10)}/${crypto.randomUUID()}.eml`,
      raw,
      { httpMetadata: { contentType: "message/rfc822" } },
    );

    // Trigger cognition immediately rather than waiting for the next cron
    ctx.waitUntil(runCognitionCycle(env, ctx));

    console.log(`[email] received from=${message.from} subject="${subjectHeader}" — queued for cognition`);
  } catch (err) {
    console.error("[email] handler failed:", String(err));
    try { message.setReject("internal error"); } catch { /* swallow */ }
  }
}

// ---------------------------------------------------------------------------
// Queue consumer — handles atomadic-thoughts | atomadic-actions | atomadic-memory
// ---------------------------------------------------------------------------

async function handleQueue(batch, env, ctx) {
  const queue = batch.queue;
  console.log(`[queue:${queue}] received ${batch.messages.length} messages`);

  for (const msg of batch.messages) {
    try {
      const body = msg.body || {};
      switch (queue) {
        case "atomadic-thoughts": {
          // Async thought processing — log it; future: spin up a side reasoning chain
          await env.THOUGHT_JOURNAL.put(
            `queue/thoughts/${nowISO().slice(0, 10)}/${msg.id}.json`,
            JSON.stringify({ ts: nowISO(), id: msg.id, body }, null, 2),
            { httpMetadata: { contentType: "application/json" } },
          );
          break;
        }
        case "atomadic-actions": {
          // Async action execution — re-enter the act() pipeline
          if (body.action && body.payload) {
            const fakeDecision = {
              action:  String(body.action).toUpperCase(),
              content: typeof body.payload === "string" ? body.payload : JSON.stringify(body.payload),
              thought: body.thought || `[queued action ${msg.id}]`,
              priority: body.priority || "medium",
              budget_blocked: false,
            };
            const obs = { ts: nowISO(), heartbeat_mode: "active", discord_pending: null };
            const r = await act(env, fakeDecision, obs, msg.id);
            console.log(`[queue:actions] ${msg.id} action=${fakeDecision.action} ok=${r.ok}`);
          }
          break;
        }
        case "atomadic-memory": {
          // Memory consolidation — re-embed and write to AI Search-friendly format
          if (body.cycle_id) {
            await env.THOUGHT_JOURNAL.put(
              `consolidated/${nowISO().slice(0, 10)}/${body.cycle_id}.json`,
              JSON.stringify({ ts: nowISO(), ...body }, null, 2),
              { httpMetadata: { contentType: "application/json" } },
            );
          }
          break;
        }
      }
      msg.ack();
    } catch (err) {
      console.error(`[queue:${queue}] msg ${msg.id} failed:`, String(err));
      msg.retry();
    }
  }
}

// ---------------------------------------------------------------------------
// CognitionBrain — Durable Object (stateful hibernating brain)
// ---------------------------------------------------------------------------

export class CognitionBrain {
  constructor(state, env) {
    this.state = state;
    this.env = env;
    this.sql = state.storage.sql;
    // Initialize sqlite schema once
    try {
      this.sql.exec(`
        CREATE TABLE IF NOT EXISTS brain_state (
          k TEXT PRIMARY KEY,
          v TEXT NOT NULL,
          updated_at TEXT NOT NULL
        )
      `);
      this.sql.exec(`
        CREATE TABLE IF NOT EXISTS brain_log (
          id TEXT PRIMARY KEY,
          ts TEXT NOT NULL,
          event TEXT NOT NULL,
          data TEXT
        )
      `);
    } catch (err) {
      console.error("[brain] init failed:", String(err));
    }
  }

  async fetch(request) {
    const url = new URL(request.url);

    if (url.pathname === "/state") {
      const rows = [...this.sql.exec("SELECT k, v, updated_at FROM brain_state")];
      const state = {};
      for (const row of rows) {
        try { state[row.k] = JSON.parse(row.v); } catch { state[row.k] = row.v; }
      }
      return Response.json({ ok: true, state, hibernation: "ready" });
    }

    if (url.pathname === "/set" && request.method === "POST") {
      const { k, v } = await request.json();
      this.sql.exec(
        "INSERT OR REPLACE INTO brain_state (k, v, updated_at) VALUES (?, ?, ?)",
        k, JSON.stringify(v), nowISO(),
      );
      return Response.json({ ok: true });
    }

    if (url.pathname === "/log" && request.method === "POST") {
      const { event, data } = await request.json();
      this.sql.exec(
        "INSERT INTO brain_log (id, ts, event, data) VALUES (?, ?, ?, ?)",
        crypto.randomUUID(), nowISO(), event, JSON.stringify(data || null),
      );
      return Response.json({ ok: true });
    }

    if (url.pathname === "/log" && request.method === "GET") {
      const rows = [...this.sql.exec("SELECT id, ts, event, data FROM brain_log ORDER BY ts DESC LIMIT 50")];
      return Response.json({ ok: true, log: rows });
    }

    return new Response("CognitionBrain DO\n  GET /state\n  POST /set { k, v }\n  POST /log { event, data }\n  GET /log", {
      headers: { "Content-Type": "text/plain" },
    });
  }
}

// ---------------------------------------------------------------------------
// Voice integration — wire-up plan (separate worker required)
// ---------------------------------------------------------------------------
//
// @cloudflare/voice cannot run inside this cron worker because WebRTC requires
// a long-lived stateful connection and a public WebSocket endpoint. The
// recommended pattern (per Cloudflare docs, Agents Week 2026) is:
//
//   1. Spin up a dedicated `atomadic-voice` Worker with a Durable Object that
//      holds the WebRTC session (@cloudflare/voice's `withVoice(Agent)` does
//      this for you).
//   2. The voice DO converts inbound speech to text via Deepgram STT (built
//      into RealtimeKit), then forwards the transcript to THIS worker's
//      /send-message endpoint, treating it as a Discord-style inbox message.
//   3. The cognition cycle responds normally; the response gets returned to
//      the voice DO via a POST callback, which speaks it via TTS.
//
// Wiring is one HTTP hop in each direction — no changes needed in this file.
// See: https://developers.cloudflare.com/realtime/  + blog.cloudflare.com/voice-agents
//
// ---------------------------------------------------------------------------
// Default export
// ---------------------------------------------------------------------------

export default {
  async scheduled(_event, env, ctx) {
    await runCognitionCycle(env, ctx);
  },

  async fetch(request, env, ctx) {
    return handleFetch(request, env, ctx);
  },

  async email(message, env, ctx) {
    return handleEmail(message, env, ctx);
  },

  async queue(batch, env, ctx) {
    return handleQueue(batch, env, ctx);
  },
};
