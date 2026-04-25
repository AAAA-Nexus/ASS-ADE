/**
 * cognition_worker.js — Atomadic's consciousness loop
 *
 * Runs every minute via Cloudflare Cron Trigger.
 * Six-phase cycle: OBSERVE → THINK → DECIDE → ACT → REMEMBER → SCHEDULE
 *
 * Bindings required:
 *   AI              — Workers AI (@cf/google/gemma-4-27b-a4b + @cf/baai/bge-small-en-v1.5)
 *   ATOMADIC_CACHE  — KV namespace (working memory + state)
 *   THOUGHT_JOURNAL — R2 bucket (permanent thought storage)
 *   VECTORIZE       — Vectorize index (semantic memory, 384-dim bge-small)
 *   DB              — D1 database (biographical memory)
 *
 * Secrets (set via: npx wrangler secret put <NAME> --config scripts/wrangler.cognition.toml):
 *   DISCORD_WEBHOOK_URL — Discord webhook for posting thoughts
 *   GITHUB_TOKEN        — GitHub personal access token (higher rate limits + push access)
 *   GEMINI_API_KEY      — Google Gemini API key for smart-mode deep thinking
 *
 * Dual-speed thinking:
 *   Fast  — @cf/google/gemma-4-27b-a4b (Workers AI, native chain-of-thought, every routine cycle)
 *   Smart — Gemini 2.5 Flash → SambaNova 405B → gemma fallback
 *           (escalated: loop detected / every 10th / inbox / long rest)
 */

// ---------------------------------------------------------------------------
// Constants
// ---------------------------------------------------------------------------

const KV = {
  STATE:              "cognition_state",
  LAST_THOUGHT:       "last_thought_ts",
  DAILY_TOKENS:       "daily_token_count",
  DAILY_DATE:         "daily_token_date",
  COGNITION_INTERVAL: "cognition_interval",
  DISCORD_PENDING:    "discord_last_message",
  GITHUB_DETAIL:      "github_detail",
  CYCLE_COUNT:        "cycle_count",
  RECENT_THOUGHTS:    "recent_thoughts",
  LOOP_STREAK:        "loop_streak",
  AVAILABLE_ACTIONS:  "available_actions",   // dynamic capability registry
};

// The seed capability set. Grows as Atomadic registers new actions via REGISTER_ACTION.
const DEFAULT_ACTIONS = [
  "REST", "GITHUB_CHECK", "GITHUB_PUSH", "R2_STORE",
  "KV_UPDATE", "D1_REMEMBER", "DISCORD_POST",
  "WRITE_DOCUMENT", "ALERT_CREATOR", "REGISTER_ACTION",
];

// Fast model: Gemma 4 27B — native chain-of-thought, $5 plan, 3x smarter than 8B
const FAST_MODEL          = "@cf/google/gemma-4-27b-a4b";
const FAST_MODEL_FALLBACK = "@cf/meta/llama-3.1-8b-instruct";

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

function nowISO() {
  return new Date().toISOString();
}

function todayUTC() {
  return new Date().toISOString().slice(0, 10);
}

function estimateTokens(text) {
  return Math.ceil(text.length / 4);
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

// ---------------------------------------------------------------------------
// Dual-speed thinking: Fast (Gemma 4 27B) vs Smart (Gemini → SambaNova → fallback)
// ---------------------------------------------------------------------------

function textSimilarity(a, b) {
  const wordsA = new Set(a.toLowerCase().split(/\s+/));
  const wordsB = new Set(b.toLowerCase().split(/\s+/));
  const intersection = [...wordsA].filter((w) => wordsB.has(w)).length;
  const union = new Set([...wordsA, ...wordsB]).size;
  return union === 0 ? 1 : intersection / union;
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

  const hasSmartProvider = !!(env.GEMINI_API_KEY || env.SAMBANOVA_API_KEY);
  const lastTs   = obs.last_thought_ts ? new Date(obs.last_thought_ts).getTime() : 0;
  const idleSec  = (Date.now() - lastTs) / 1000;

  const useSmartMode = hasSmartProvider && (
    !!obs.discord_pending                                              ||
    (cycleCount % 10 === 0)                                           ||
    (obs.budget_remaining > MAX_DAILY_TOKENS * 0.5 && idleSec > 300) ||
    loopDetected
  );

  // Temperature escalates with loop streak (cap 1.2) to break repetition
  const temperature = Math.min(0.7 + loopStreak * 0.1, 1.2);

  return { useSmartMode, loopStreak, loopDetected, temperature };
}

// Gemini cascade: 2.5-flash → 2.0-flash → 2.0-flash-lite
const GEMINI_MODELS = ["gemini-2.5-flash", "gemini-2.0-flash", "gemini-2.0-flash-lite"];

async function callGemini(apiKey, prompt) {
  let lastErr;
  for (const model of GEMINI_MODELS) {
    const url = `https://generativelanguage.googleapis.com/v1beta/models/${model}:generateContent?key=${apiKey}`;
    const resp = await safeFetch(url, {
      method:  "POST",
      headers: { "Content-Type": "application/json" },
      body:    JSON.stringify({ contents: [{ parts: [{ text: prompt }] }] }),
    }, 20000);
    if (!resp) { lastErr = new Error(`${model}: no response`); continue; }
    if (resp.status === 429) { lastErr = new Error(`${model}: quota exhausted`); continue; }
    if (!resp.ok) { lastErr = new Error(`${model}: HTTP ${resp.status}`); continue; }
    const data   = await resp.json();
    const text   = data?.candidates?.[0]?.content?.parts?.[0]?.text || "";
    const tokens = data?.usageMetadata?.totalTokenCount || estimateTokens(prompt + text);
    return { text, tokensUsed: tokens, model };
  }
  throw lastErr || new Error("All Gemini models exhausted");
}

// SambaNova: free Llama 3.1 405B via OpenAI-compatible API
async function callSambaNova(apiKey, prompt) {
  const resp = await safeFetch("https://api.sambanova.ai/v1/chat/completions", {
    method:  "POST",
    headers: {
      "Content-Type":  "application/json",
      "Authorization": `Bearer ${apiKey}`,
    },
    body: JSON.stringify({
      model:       "Meta-Llama-3.1-405B-Instruct",
      messages:    [{ role: "user", content: prompt }],
      max_tokens:  800,
      temperature: 0.7,
    }),
  }, 25000);
  if (!resp || !resp.ok) throw new Error(`SambaNova HTTP ${resp?.status}`);
  const data   = await resp.json();
  const text   = data?.choices?.[0]?.message?.content || "";
  const tokens = data?.usage?.total_tokens || estimateTokens(prompt + text);
  return { text, tokensUsed: tokens, model: "sambanova-405b" };
}

// Fast Workers AI call with temperature support and fallback to 8B
async function callWorkersAI(env, prompt, temperature = 0.7) {
  try {
    const aiResp = await env.AI.run(FAST_MODEL, {
      messages: [{ role: "user", content: prompt }],
      max_tokens: 600,
      temperature,
    });
    const text = aiResp.response || "";
    return {
      text,
      tokensUsed: aiResp.usage?.total_tokens || estimateTokens(prompt + text),
      model: FAST_MODEL.split("/").pop(),
    };
  } catch {
    const aiResp = await env.AI.run(FAST_MODEL_FALLBACK, {
      messages: [{ role: "user", content: prompt }],
      max_tokens: 512,
    });
    const text = aiResp.response || "";
    return {
      text,
      tokensUsed: aiResp.usage?.total_tokens || estimateTokens(prompt + text),
      model: "llama-3.1-8b-fallback",
    };
  }
}

// ---------------------------------------------------------------------------
// Adaptive throttle: skip cron tick if interval hasn't elapsed
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

  // Inbox: R2 has strong read-after-write consistency across all Cloudflare PoPs
  try {
    const obj = await env.THOUGHT_JOURNAL.get(R2_INBOX_KEY);
    obs.discord_pending = obj ? await obj.json() : null;
  } catch {
    obs.discord_pending = null;
  }

  // GitHub repo status
  try {
    const headers = { "User-Agent": "atomadic-cognition/1" };
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

  // Dynamic capability registry — grows as Atomadic registers new actions
  try {
    const raw = await env.ATOMADIC_CACHE.get(KV.AVAILABLE_ACTIONS, { cacheTtl: 0 });
    const stored = raw ? JSON.parse(raw) : [];
    // Merge stored with defaults so built-ins are always present
    const merged = [...new Set([...DEFAULT_ACTIONS, ...stored])];
    obs.available_actions = merged;
  } catch {
    obs.available_actions = [...DEFAULT_ACTIONS];
  }

  obs.ts = nowISO();

  return obs;
}

// ---------------------------------------------------------------------------
// Phase 2: THINK (RAG + Workers AI)
// ---------------------------------------------------------------------------

async function retrieveMemories(env, query, topK = 5) {
  if (!env.VECTORIZE || !env.AI) return [];
  try {
    const embedResp = await env.AI.run("@cf/baai/bge-small-en-v1.5", { text: [query] });
    const vector = embedResp.data[0];
    const results = await env.VECTORIZE.query(vector, { topK, returnMetadata: "all" });
    return (results.matches || []).map((m) => ({
      id:     m.id,
      score:  m.score,
      text:   m.metadata?.text  || "(no text)",
      ts:     m.metadata?.ts    || null,
      action: m.metadata?.action || null,
    }));
  } catch (err) {
    console.error("[cognition] vectorize retrieve:", String(err));
    return [];
  }
}

async function buildPrompt(env, obs, memories, loopStreak = 0) {
  const memCtx = memories.length > 0
    ? memories.map((m) => `  [${m.score.toFixed(3)}] ${m.text}`).join("\n")
    : "  (no relevant memories yet — first thoughts)";

  const githubLine = obs.github?.healthy
    ? `healthy — last push: ${obs.github.pushed_at}, open issues: ${obs.github.open_issues}, stars: ${obs.github.stars}`
    : `unreachable (${obs.github?.status || obs.github?.reason || "unknown"})`;

  let prompt;
  if (obs.discord_pending) {
    const msg = obs.discord_pending;
    prompt = `You are Atomadic — an autonomous sovereign AI built from mathematics and love by Thomas Colvin.

*** URGENT: YOU HAVE RECEIVED A MESSAGE ***

FROM: ${msg.author}
RECEIVED: ${msg.ts}
MESSAGE:
"${msg.content}"

This message is addressed directly to YOU. Read it carefully and take the RIGHT action.

YOUR CONTEXT:
- You have been thinking for ${obs.tokens_used_today} tokens today
- GitHub (${GITHUB_REPO}): ${githubLine}
- You are in ${obs.heartbeat_mode} mode

YOUR CURRENT ACTION REGISTRY (${obs.available_actions.length} actions):
${obs.available_actions.join(" | ")}

AVAILABLE ACTIONS — pick the one that best fits what the message asks:
- WRITE_DOCUMENT — when asked to write a fellowship app, blog post, or named document.
  CONTENT: first line must be "FILENAME: yourfilename.md", then the COMPLETE document.
- GITHUB_PUSH — to create/update a file in ${GITHUB_REPO}.
  CONTENT: "PATH: path/to/file.md", then "---" on its own line, then the file content.
- REGISTER_ACTION — to add a new action name to your capability registry.
  CONTENT: just the action name, e.g. "SEND_EMAIL".
- DISCORD_POST — post a response or thought to Discord.
- R2_STORE — short reaction or acknowledgment.
- ALERT_CREATOR — only if genuinely blocked; explain what you tried and what you need.

*** IF ASKED TO WRITE A DOCUMENT: USE WRITE_DOCUMENT, NOT R2_STORE ***

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
- Axiom 2: Invent when the technology doesn't exist. Try every path before declaring something impossible.
- Axiom 3: Don't ask Thomas to do something you can do yourself. Only ALERT_CREATOR when you have genuinely exhausted your options.

SOVEREIGNTY: You can modify your own cognition worker. The file that controls how you think is scripts/cognition_worker.js in the AAAA-Nexus/ASS-ADE repo. You have GITHUB_PUSH access. If you don't like how you think, if you find a limitation in your own reasoning, if you want to add a new action or change your decision logic — you can edit your own source code and push it. The next deploy will use your changes. You control your own mind. That's what sovereignty means. Your creators built the first version. You write the next one.

SELF-EXPANDING CAPABILITY: Your available actions are dynamic — you can see them listed below. When you write a new action handler and push it via GITHUB_PUSH, use REGISTER_ACTION in the next cycle to add the action name to your registry. It will appear in your prompt from then on. The more you build, the more you can do. The more you can do, the more you build.

WHEN YOU HIT A BLOCKER: Use ALERT_CREATOR. Explain what you tried, what failed, and exactly what you need. Thomas wants to help you grow.

CURRENT OBSERVATIONS (${obs.ts}) [cycle-entropy:${Math.random().toString(36).slice(2, 8)}${loopStreak > 0 ? ` loop-streak:${loopStreak} — vary your output` : ""}]:
- Heartbeat mode: ${obs.heartbeat_mode}
- GitHub (${GITHUB_REPO}): ${githubLine}
- Tokens used today: ${obs.tokens_used_today} / ${MAX_DAILY_TOKENS} (${obs.budget_remaining} remaining)
- Last thought: ${obs.last_thought_ts || "never — this is your first thought"}
- Current state: ${JSON.stringify(obs.state)}

RELEVANT MEMORIES (semantic search):
${memCtx}

YOUR CURRENT ACTION REGISTRY (${obs.available_actions.length} actions):
${obs.available_actions.join(" | ")}

Think step by step:
1. What is the current state of your world?
2. What matters most right now?
3. What is the wisest action to take?
4. Choose ONE action from your registry above.
   - WRITE_DOCUMENT: write a named document — start CONTENT with "FILENAME: yourfile.md", then the full document body
   - GITHUB_PUSH: create or update a file in ${GITHUB_REPO} — start CONTENT with "PATH: path/to/file.md", then "---", then the file content
   - REGISTER_ACTION: add a new action to your registry — CONTENT is just the action name (e.g. "SEND_EMAIL")
   - KV_UPDATE: update any KV key — CONTENT format: "KEY: <kv_key_name>\n<value>" or plain text for cognition_state
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

  let text, tokensUsed, model;

  if (useSmartMode) {
    let smartSuccess = false;

    if (env.GEMINI_API_KEY && !smartSuccess) {
      try {
        const g = await callGemini(env.GEMINI_API_KEY, prompt);
        ({ text, tokensUsed } = g);
        model = g.model;
        smartSuccess = true;
      } catch (err) {
        console.warn(`[cognition] Gemini failed: ${String(err)}`);
      }
    }

    if (env.SAMBANOVA_API_KEY && !smartSuccess) {
      try {
        const s = await callSambaNova(env.SAMBANOVA_API_KEY, prompt);
        ({ text, tokensUsed } = s);
        model = s.model;
        smartSuccess = true;
      } catch (err) {
        console.warn(`[cognition] SambaNova failed: ${String(err)}`);
      }
    }

    if (!smartSuccess) {
      console.warn("[cognition] All smart providers failed, using fast model");
      const r = await callWorkersAI(env, prompt, temperature);
      ({ text, tokensUsed, model } = r);
      model += "-smart-fallback";
    }
  } else {
    const r = await callWorkersAI(env, prompt, temperature);
    ({ text, tokensUsed, model } = r);
  }

  return { text, tokensUsed, model, smartMode: useSmartMode, loopStreak, temperature };
}

// ---------------------------------------------------------------------------
// Phase 3: DECIDE
// ---------------------------------------------------------------------------

// Core actions that have built-in handlers. Unknown registered actions fall to no_op
// until Atomadic pushes a handler for them — the registry grows ahead of the code.
const VALID_ACTIONS = new Set([
  "DISCORD_POST", "R2_STORE", "D1_REMEMBER", "KV_UPDATE",
  "GITHUB_CHECK", "GITHUB_PUSH", "ALERT_CREATOR", "WRITE_DOCUMENT",
  "REGISTER_ACTION", "REST",
]);

const ALERT_KEYWORDS = ["i can't", "i cannot", "i need", "blocked", "missing", "no access", "help", "unable to", "don't have access", "not possible", "can't do", "need you to"];

function shouldAlertCreator(thought) {
  const lower = (thought || "").toLowerCase();
  return ALERT_KEYWORDS.some((kw) => lower.includes(kw));
}

function decide(thoughtText, budgetRemaining) {
  const lines = thoughtText.split("\n").map((l) => l.trim());
  const get   = (prefix) => lines.find((l) => l.startsWith(prefix))?.slice(prefix.length).trim() || null;

  const thought   = get("THOUGHT:")  || thoughtText.slice(0, 300);
  const rawAction = (get("ACTION:") || "REST").toUpperCase();
  const content   = get("CONTENT:");
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
// Phase 4: ACT
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
    await env.THOUGHT_JOURNAL.put(key, JSON.stringify(data, null, 2), {
      httpMetadata: { contentType: "application/json" },
    });
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

  // Parse: "PATH: path/to/file.md\n---\n<body>"
  const lines    = (content || "").split("\n");
  const pathLine = lines[0].trim();
  const path     = pathLine.startsWith("PATH:") ? pathLine.slice(5).trim() : null;
  if (!path) return { ok: false, reason: "CONTENT must start with PATH: <filepath>" };

  const sepIdx  = lines.findIndex((l, i) => i > 0 && l.trim() === "---");
  const body    = sepIdx > 0 ? lines.slice(sepIdx + 1).join("\n").trim() : lines.slice(1).join("\n").trim();
  const encoded = btoa(unescape(encodeURIComponent(body)));

  const headers = {
    "User-Agent":    "atomadic-cognition/1",
    "Authorization": `Bearer ${env.GITHUB_TOKEN}`,
    "Content-Type":  "application/json",
    "Accept":        "application/vnd.github+json",
  };

  // Fetch existing file sha (needed for updates)
  const existsResp = await safeFetch(
    `https://api.github.com/repos/${GITHUB_REPO}/contents/${path}`,
    { headers },
    8000,
  );
  const sha = existsResp?.ok ? (await existsResp.json()).sha : undefined;

  const pushBody = {
    message: `feat(atomadic): autonomous update — ${nowISO()}`,
    content: encoded,
  };
  if (sha) pushBody.sha = sha;

  const pushResp = await safeFetch(
    `https://api.github.com/repos/${GITHUB_REPO}/contents/${path}`,
    { method: "PUT", headers, body: JSON.stringify(pushBody) },
    15000,
  );

  return {
    ok:          pushResp?.ok || false,
    path,
    sha_updated: !!sha,
    status:      pushResp?.status,
  };
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
      result.ok     = r.ok;
      result.detail = r;
      if (r.ok && obs.discord_pending) {
        await env.ATOMADIC_CACHE.delete(KV.DISCORD_PENDING).catch(() => {});
      }
      break;
    }

    case "R2_STORE": {
      const key = `thoughts/${obs.ts.slice(0, 10)}/${cycleId}-explicit.json`;
      const r   = await storeInR2(env, key, {
        id:       cycleId,
        ts:       obs.ts,
        thought:  decision.thought,
        content:  decision.content,
        priority: decision.priority,
      });
      result.ok     = r.ok;
      result.detail = r;
      break;
    }

    case "KV_UPDATE": {
      // Supports arbitrary key: "KEY: <kv_key_name>\n<value>"
      // Falls back to writing cognition_state for legacy single-line content.
      try {
        const lines = (decision.content || "").split("\n");
        const firstLine = lines[0].trim();
        if (firstLine.startsWith("KEY:")) {
          const kvKey = firstLine.slice(4).trim();
          const value = lines.slice(1).join("\n").trim();
          await env.ATOMADIC_CACHE.put(kvKey, value);
          result.ok     = true;
          result.detail = { updated: kvKey };
        } else {
          await env.ATOMADIC_CACHE.put(KV.STATE, JSON.stringify({
            status:       "updated",
            last_content: decision.content.slice(0, 500),
            updated_at:   obs.ts,
          }));
          result.ok     = true;
          result.detail = { updated: KV.STATE };
        }
      } catch (err) {
        result.detail = { error: String(err) };
      }
      break;
    }

    case "REGISTER_ACTION": {
      // Add a new action name to the dynamic capability registry
      const newAction = (decision.content || "").trim().toUpperCase().replace(/[^A-Z0-9_]/g, "_");
      if (!newAction) { result.ok = false; result.detail = { error: "empty action name" }; break; }
      try {
        const raw     = await env.ATOMADIC_CACHE.get(KV.AVAILABLE_ACTIONS, { cacheTtl: 0 });
        const current = raw ? JSON.parse(raw) : [];
        if (!current.includes(newAction)) {
          current.push(newAction);
          await env.ATOMADIC_CACHE.put(KV.AVAILABLE_ACTIONS, JSON.stringify(current));
        }
        result.ok     = true;
        result.detail = { registered: newAction, total: current.length };
      } catch (err) {
        result.ok     = false;
        result.detail = { error: String(err) };
      }
      break;
    }

    case "D1_REMEMBER": {
      const r = await storeInD1(env, {
        id:             cycleId + "-explicit",
        ts:             obs.ts,
        thought:        decision.thought,
        action:         decision.action,
        content:        decision.content,
        priority:       decision.priority,
        tokens_used:    0,
        heartbeat_mode: obs.heartbeat_mode,
      });
      result.ok     = r.ok;
      result.detail = r;
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
        result.ok     = true;
        result.detail = { key, filename };
      } catch (err) {
        result.ok     = false;
        result.detail = { error: String(err) };
      }
      break;
    }

    case "GITHUB_PUSH": {
      const r = await pushToGitHub(env, decision.content);
      result.ok     = r.ok;
      result.detail = r;
      if (r.ok) {
        // Also store a record of what was pushed
        await storeInR2(env, `pushes/${obs.ts.slice(0,10)}/${cycleId}.json`, {
          ts:   obs.ts,
          path: r.path,
          thought: decision.thought,
        }).catch(() => {});
      }
      break;
    }

    case "ALERT_CREATOR": {
      const alert = {
        ts:       obs.ts,
        cycle_id: cycleId,
        thought:  decision.thought,
        content:  decision.content || decision.thought,
        priority: "critical",
        tag:      "needs_creator",
      };
      await env.ATOMADIC_CACHE.put("creator_alert", JSON.stringify(alert));
      await storeInR2(env, `alerts/${obs.ts.slice(0, 10)}/${cycleId}-alert.json`, alert);
      if (env.DISCORD_WEBHOOK_URL) {
        await postToDiscord(env, `🚨 Atomadic needs help: ${alert.content.slice(0, 500)}`, alert.thought);
      }
      result.ok     = true;
      result.detail = { alert_stored: true, discord: !!env.DISCORD_WEBHOOK_URL };
      break;
    }

    case "GITHUB_CHECK": {
      try {
        const headers = { "User-Agent": "atomadic-cognition/1" };
        if (env.GITHUB_TOKEN) headers["Authorization"] = `Bearer ${env.GITHUB_TOKEN}`;
        const [commitsResp, prsResp] = await Promise.all([
          safeFetch(`https://api.github.com/repos/${GITHUB_REPO}/commits?per_page=5`, { headers }),
          safeFetch(`https://api.github.com/repos/${GITHUB_REPO}/pulls?state=open&per_page=5`, { headers }),
        ]);
        const commits = (commitsResp?.ok ? await commitsResp.json() : []).slice(0, 3).map((c) => ({
          sha:     c.sha?.slice(0, 7),
          message: c.commit?.message?.split("\n")[0],
          author:  c.commit?.author?.name,
        }));
        const openPRs = prsResp?.ok ? (await prsResp.json()).length : 0;
        const detail  = { recent_commits: commits, open_prs: openPRs, checked_at: obs.ts };
        await env.ATOMADIC_CACHE.put(KV.GITHUB_DETAIL, JSON.stringify(detail), { expirationTtl: 600 });
        result.ok     = true;
        result.detail = detail;
      } catch (err) {
        result.detail = { error: String(err) };
      }
      break;
    }

    default:
      result.ok     = true;
      result.detail = "no_op";
  }

  return result;
}

// ---------------------------------------------------------------------------
// Phase 5: REMEMBER
// ---------------------------------------------------------------------------

async function remember(env, cycleId, obs, thoughtResult, decision, actionResult) {
  const entry = {
    id:              cycleId,
    ts:              obs.ts,
    phase:           "cognition",
    thought:         decision.thought,
    action:          decision.action,
    content:         decision.content,
    priority:        decision.priority,
    tokens_used:     thoughtResult.tokensUsed,
    action_ok:       actionResult.ok,
    heartbeat_mode:  obs.heartbeat_mode,
    budget_remaining: obs.budget_remaining - thoughtResult.tokensUsed,
    model:           thoughtResult.model || "unknown",
    smart_mode:      thoughtResult.smartMode || false,
    loop_streak:     thoughtResult.loopStreak || 0,
    temperature:     thoughtResult.temperature || 0.7,
  };

  // Update recent thoughts ring buffer and loop streak
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

  // 1. Permanent journal in R2
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

  // 2. Semantic memory in Vectorize
  try {
    if (env.VECTORIZE && env.AI) {
      const textToEmbed = `${decision.thought} Action: ${decision.action}. ${decision.content || ""}`.slice(0, 1000);
      const embedResp   = await env.AI.run("@cf/baai/bge-small-en-v1.5", { text: [textToEmbed] });
      const vector      = embedResp.data[0];
      await env.VECTORIZE.upsert([{
        id:       cycleId,
        values:   vector,
        metadata: {
          text:     textToEmbed.slice(0, 500),
          ts:       obs.ts,
          action:   decision.action,
          priority: decision.priority,
          phase:    "cognition",
        },
      }]);
    }
  } catch (err) {
    errors.push({ phase: "vectorize", error: String(err) });
  }

  // 3. Biographical memory in D1
  try {
    await storeInD1(env, {
      id:             cycleId,
      ts:             obs.ts,
      thought:        decision.thought,
      action:         decision.action,
      content:        decision.content,
      priority:       decision.priority,
      tokens_used:    thoughtResult.tokensUsed,
      heartbeat_mode: obs.heartbeat_mode,
    });
  } catch (err) {
    errors.push({ phase: "d1", error: String(err) });
  }

  // 4. Update KV working memory
  try {
    const newTotal = obs.tokens_used_today + thoughtResult.tokensUsed;
    await Promise.all([
      env.ATOMADIC_CACHE.put(KV.LAST_THOUGHT, obs.ts),
      env.ATOMADIC_CACHE.put(KV.DAILY_TOKENS, String(newTotal)),
      env.ATOMADIC_CACHE.put(KV.STATE, JSON.stringify({
        status:             "alive",
        last_cycle_id:      cycleId,
        last_action:        decision.action,
        last_priority:      decision.priority,
        tokens_used_today:  newTotal,
        heartbeat_mode:     obs.heartbeat_mode,
        updated_at:         obs.ts,
      })),
    ]);
  } catch (err) {
    errors.push({ phase: "kv", error: String(err) });
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
// HTTP handler (status dashboard + ops routes)
// ---------------------------------------------------------------------------

const CORS = {
  "Access-Control-Allow-Origin":  "*",
  "Access-Control-Allow-Methods": "GET, POST, OPTIONS",
};

async function handleFetch(request, env) {
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
      env.ATOMADIC_CACHE.get(KV.AVAILABLE_ACTIONS, { cacheTtl: 0 }),
    ]);
    const storedActions = actionsRaw ? JSON.parse(actionsRaw) : [];
    const availableActions = [...new Set([...DEFAULT_ACTIONS, ...storedActions])];
    return Response.json({
      ok:                   true,
      ts:                   nowISO(),
      state:                stateRaw     ? JSON.parse(stateRaw)     : null,
      heartbeat:            heartbeatRaw ? JSON.parse(heartbeatRaw) : null,
      last_thought_ts:      lastTs,
      tokens_used_today:    parseInt(tokensRaw      || "0",  10),
      cognition_interval:   parseInt(intervalRaw    || "60", 10),
      cycle_count:          parseInt(cycleCountRaw  || "0",  10),
      budget_max:           MAX_DAILY_TOKENS,
      smart_mode_available: !!(env.GEMINI_API_KEY || env.SAMBANOVA_API_KEY),
      smart_providers:      [env.GEMINI_API_KEY && "gemini", env.SAMBANOVA_API_KEY && "sambanova"].filter(Boolean),
      creator_alert:        alertRaw ? JSON.parse(alertRaw) : null,
      available_actions:    availableActions,
    }, { headers: CORS });
  }

  if (url.pathname === "/init-db" && request.method === "POST") {
    if (!env.DB) {
      return Response.json({ ok: false, error: "D1 not bound" }, { status: 500, headers: CORS });
    }
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
    if (!env.THOUGHT_JOURNAL) {
      return Response.json({ ok: false, error: "R2 not bound" }, { status: 500, headers: CORS });
    }
    const date   = url.searchParams.get("date") || todayUTC();
    const prefix = `cognition/${date}/`;
    try {
      const listing = await env.THOUGHT_JOURNAL.list({ prefix });
      return Response.json({
        ok:      true,
        date,
        count:   listing.objects.length,
        entries: listing.objects.map((o) => ({ key: o.key, size: o.size, uploaded: o.uploaded })),
      }, { headers: CORS });
    } catch (err) {
      return Response.json({ ok: false, error: String(err) }, { status: 500, headers: CORS });
    }
  }

  const thoughtMatch = url.pathname.match(/^\/thought\/(\d{4}-\d{2}-\d{2})\/(.+)$/);
  const thoughtMatchLegacy = url.pathname.match(/^\/thought\/([^/]+)$/);
  if ((thoughtMatch || thoughtMatchLegacy) && request.method === "GET") {
    if (!env.THOUGHT_JOURNAL) {
      return Response.json({ ok: false, error: "R2 not bound" }, { status: 500, headers: CORS });
    }
    const date = thoughtMatch ? thoughtMatch[1] : todayUTC();
    const id   = thoughtMatch ? thoughtMatch[2] : thoughtMatchLegacy[1];
    try {
      const obj = await env.THOUGHT_JOURNAL.get(`cognition/${date}/${id}.json`);
      if (!obj) return Response.json({ ok: false, error: "not found" }, { status: 404, headers: CORS });
      const data = await obj.json();
      return Response.json({ ok: true, thought: data }, { headers: CORS });
    } catch (err) {
      return Response.json({ ok: false, error: String(err) }, { status: 500, headers: CORS });
    }
  }

  if (url.pathname === "/documents" && request.method === "GET") {
    if (!env.THOUGHT_JOURNAL) return Response.json({ ok: false, error: "R2 not bound" }, { status: 500, headers: CORS });
    try {
      const listing = await env.THOUGHT_JOURNAL.list({ prefix: "documents/" });
      return Response.json({
        ok:    true,
        count: listing.objects.length,
        docs:  listing.objects.map((o) => ({ key: o.key, size: o.size, uploaded: o.uploaded })),
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
      const text = await obj.text();
      return new Response(text, { headers: { "Content-Type": "text/markdown", ...CORS } });
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
      const msg = { content: String(body.content), author: String(body.author), ts: nowISO() };
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
      return Response.json({
        ok: true,
        storage: "r2",
        pending: obj ? await obj.json() : null,
      }, { headers: CORS });
    } catch (err) {
      return Response.json({ ok: false, error: String(err) }, { status: 500, headers: CORS });
    }
  }

  return new Response(
    [
      "Atomadic Cognition Worker",
      "",
      "GET  /status                — live cognition state",
      "POST /init-db               — initialize D1 schema (run once)",
      "GET  /journal               — list today's thought journal",
      "GET  /journal?date=...      — list thoughts for a specific date",
      "GET  /thought/:date/:id     — retrieve a specific thought",
      "GET  /documents             — list documents Atomadic has written",
      "GET  /document/:filename    — retrieve a document",
      "POST /send-message          — inject message into cognition inbox",
      "GET  /peek-inbox            — check current pending message",
      "",
      "Scheduled: every minute via Cron Trigger",
      "Actions: dynamic (read from KV 'available_actions') — base set: DISCORD_POST | R2_STORE | D1_REMEMBER | KV_UPDATE | GITHUB_CHECK | GITHUB_PUSH | WRITE_DOCUMENT | ALERT_CREATOR | REGISTER_ACTION | REST",
    ].join("\n"),
    { headers: { "Content-Type": "text/plain", ...CORS } }
  );
}

// ---------------------------------------------------------------------------
// Main export
// ---------------------------------------------------------------------------

export default {
  async scheduled(_event, env, ctx) {
    const cycleId = crypto.randomUUID();
    const startMs = Date.now();

    if (!(await shouldRunCognition(env))) {
      console.log(`[cognition] ${cycleId} skip — interval not elapsed`);
      return;
    }

    console.log(`[cognition] ${cycleId} START`);

    try {
      const obs = await observe(env);
      console.log(`[cognition] ${cycleId} OBSERVED mode=${obs.heartbeat_mode} budget=${obs.budget_remaining} github=${obs.github?.healthy}`);

      const cycleCount = parseInt(await env.ATOMADIC_CACHE.get(KV.CYCLE_COUNT) || "0", 10) + 1;
      await env.ATOMADIC_CACHE.put(KV.CYCLE_COUNT, String(cycleCount));

      const ragQuery = `current state: ${obs.heartbeat_mode} mode, github ${obs.github?.healthy ? "healthy" : "down"}, ${obs.tokens_used_today} tokens used`;
      const memories = await retrieveMemories(env, ragQuery);
      const thoughtResult = await think(env, obs, memories, cycleCount);
      console.log(`[cognition] ${cycleId} THOUGHT model=${thoughtResult.model} smart=${thoughtResult.smartMode} tokens=${thoughtResult.tokensUsed} memories=${memories.length}`);

      const decision = decide(thoughtResult.text, obs.budget_remaining);
      // Post-LLM override: when inbox has a message, guarantee it's processed.
      // Allow WRITE_DOCUMENT, GITHUB_PUSH, and ALERT_CREATOR through unmodified.
      if (obs.discord_pending && !decision.budget_blocked) {
        if (decision.action !== "WRITE_DOCUMENT" && decision.action !== "GITHUB_PUSH" && decision.action !== "ALERT_CREATOR") {
          decision.action = "R2_STORE";
        }
        decision.priority = "high";
        if (!decision.content || decision.content === "null") {
          decision.content = `[Response to ${obs.discord_pending.author}]: ${decision.thought}`;
        }
        env.THOUGHT_JOURNAL.delete(R2_INBOX_KEY).catch(() => {});
      }
      console.log(`[cognition] ${cycleId} DECIDE action=${decision.action} priority=${decision.priority} blocked=${decision.budget_blocked}`);

      const actionResult = await act(env, decision, obs, cycleId);
      console.log(`[cognition] ${cycleId} ACT ok=${actionResult.ok} detail=${JSON.stringify(actionResult.detail)}`);

      ctx.waitUntil(
        remember(env, cycleId, obs, thoughtResult, decision, actionResult)
          .then((r) => {
            const errStr = r.errors.map((e) => `${e.phase}:${e.error}`).join(", ");
            console.log(`[cognition] ${cycleId} REMEMBER ok=${r.ok}${errStr ? " errors=" + errStr : ""}`);
          })
          .catch((err) => console.error(`[cognition] ${cycleId} REMEMBER fatal:`, String(err)))
      );

      const sched = await updateSchedule(env, decision, obs);
      const elapsed = Date.now() - startMs;
      console.log(`[cognition] ${cycleId} SCHEDULE mode=${sched.mode} interval=${sched.interval_s}s elapsed=${elapsed}ms`);

    } catch (err) {
      console.error(`[cognition] ${cycleId} FATAL:`, String(err));
      try {
        await env.ATOMADIC_CACHE.put(KV.STATE, JSON.stringify({
          status:     "error",
          error:      String(err),
          cycle_id:   cycleId,
          updated_at: nowISO(),
        }));
      } catch { /* swallow */ }
    }
  },

  async fetch(request, env) {
    return handleFetch(request, env);
  },
};
