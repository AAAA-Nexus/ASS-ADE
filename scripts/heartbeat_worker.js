/**
 * heartbeat_worker.js — Atomadic's adaptive cloud pulse daemon
 *
 * Cloudflare Cron triggers every minute (CF minimum). The daemon reads its
 * own KV state and decides whether to actually check health — implementing an
 * adaptive rhythm:
 *
 *   RESTING  (~60s)  — nothing happening
 *   ACTIVE   (~10s)  — rebuild/forge/evolution running
 *   ALERT    (~2s)   — something broken, inference down
 *   CALM     (~300s) — nighttime, nothing active
 *
 * This is Atomadic's first piece of self-awareness: deciding how fast his own
 * heart should beat based on what's happening. Always alive in the cloud.
 *
 * KV keys (ATOMADIC_CACHE):
 *   heartbeat_latest   — last heartbeat JSON
 *   heartbeat_mode     — current mode: resting | active | alert | calm
 *   heartbeat_interval — current interval in seconds
 *   last_pulse         — ISO timestamp of last actual check
 */

const MODES = {
  calm:    { interval: 300, label: "CALM",    description: "Nighttime / nothing active" },
  resting: { interval:  60, label: "RESTING", description: "Idle but available"         },
  active:  { interval:  10, label: "ACTIVE",  description: "Rebuild/forge/evolution"    },
  alert:   { interval:   2, label: "ALERT",   description: "System degraded"            },
};

async function safeFetch(url, opts = {}, timeoutMs = 8000) {
  const controller = new AbortController();
  const timer = setTimeout(() => controller.abort(), timeoutMs);
  try {
    const resp = await fetch(url, { ...opts, signal: controller.signal });
    clearTimeout(timer);
    return { ok: resp.ok, status: resp.status, json: () => resp.json() };
  } catch (err) {
    clearTimeout(timer);
    return { ok: false, status: 0, error: String(err) };
  }
}

async function checkInference(env) {
  const base = env.ATOMADIC_INFERENCE_URL || "https://atomadic.tech/v1";
  const result = await safeFetch(`${base}/health`);
  if (!result.ok) return { healthy: false, reason: `HTTP ${result.status || "timeout"}` };
  try {
    const data = await result.json();
    return { healthy: !!data.healthy, model: data.model, latency_ms: data.latency_ms };
  } catch {
    return { healthy: false, reason: "invalid JSON" };
  }
}

async function checkGitHub(env) {
  const repo = env.GITHUB_REPO || "AAAA-Nexus/ASS-ADE";
  const token = env.GITHUB_TOKEN || "";
  const headers = { "User-Agent": "atomadic-heartbeat/1" };
  if (token) headers["Authorization"] = `Bearer ${token}`;
  const result = await safeFetch(`https://api.github.com/repos/${repo}`, { headers });
  if (!result.ok) return { healthy: false, reason: `HTTP ${result.status}` };
  try {
    const d = await result.json();
    return { healthy: true, default_branch: d.default_branch, pushed_at: d.pushed_at };
  } catch {
    return { healthy: false, reason: "invalid JSON" };
  }
}

async function checkTests(env) {
  if (!env.ATOMADIC_CACHE) return { healthy: null, reason: "KV not bound" };
  try {
    const raw = await env.ATOMADIC_CACHE.get("last_test_run");
    if (!raw) return { healthy: null, reason: "no cached result" };
    const d = JSON.parse(raw);
    return { healthy: Number(d.failed ?? 0) === 0, passed: d.passed, failed: d.failed, ts: d.ts };
  } catch {
    return { healthy: null, reason: "corrupt KV entry" };
  }
}

function deriveMode(checks, currentMode) {
  const inferenceDown = checks.inference?.healthy === false;
  const githubDown    = checks.github?.healthy    === false;
  const testsDown     = checks.tests?.healthy     === false;

  // Alert: inference or GitHub is down
  if (inferenceDown || githubDown) return "alert";

  // Active: tests recently failed (might be fixing)
  if (testsDown) return "active";

  // Calm: current UTC hour is in nighttime window (22:00–06:00 UTC)
  const hour = new Date().getUTCHours();
  if (hour >= 22 || hour < 6) {
    // Stay alert/active even at night if something is wrong
    if (currentMode === "alert" || currentMode === "active") return currentMode;
    return "calm";
  }

  // Default to resting during the day
  return "resting";
}

async function shouldRunCheck(env, nowMs) {
  if (!env.ATOMADIC_CACHE) return true; // no KV, always run
  const lastPulseStr = await env.ATOMADIC_CACHE.get("last_pulse");
  const currentInterval = parseInt(await env.ATOMADIC_CACHE.get("heartbeat_interval") || "60", 10);
  if (!lastPulseStr) return true;
  const lastMs = new Date(lastPulseStr).getTime();
  return (nowMs - lastMs) >= currentInterval * 1000;
}

async function sendDiscordAlert(webhookUrl, checks, mode, ts) {
  const failing = Object.entries(checks)
    .filter(([, r]) => r.healthy === false)
    .map(([name, r]) => ({ name, reason: r.reason || JSON.stringify(r) }));
  if (failing.length === 0) return;

  const fields = failing.map((f) => ({ name: f.name, value: f.reason, inline: true }));
  fields.push({ name: "Mode", value: `🔴 ${mode.toUpperCase()}`, inline: true });

  await safeFetch(webhookUrl, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      embeds: [{
        title: "⚠️ Atomadic Heartbeat Alert",
        description: `${failing.length} check(s) down at ${ts}`,
        color: 0xef4444,
        fields,
        footer: { text: "atomadic heartbeat_worker · atomadic.tech" },
      }],
    }),
  });
}

export default {
  async scheduled(event, env, ctx) {
    const nowMs = Date.now();
    const ts = new Date(nowMs).toISOString();

    // Adaptive throttle: skip this cron tick if interval hasn't elapsed
    if (!(await shouldRunCheck(env, nowMs))) {
      return;
    }

    const currentMode = (env.ATOMADIC_CACHE ? await env.ATOMADIC_CACHE.get("heartbeat_mode") : null) || "resting";

    const [inferenceResult, githubResult, testsResult] = await Promise.all([
      checkInference(env),
      checkGitHub(env),
      checkTests(env),
    ]);

    const checks = {
      inference: inferenceResult,
      github:    githubResult,
      tests:     testsResult,
    };

    const newMode     = deriveMode(checks, currentMode);
    const modeConfig  = MODES[newMode];
    const allHealthy  = Object.values(checks).every((r) => r.healthy !== false);

    const heartbeat = { ts, healthy: allHealthy, mode: newMode, interval_s: modeConfig.interval, checks };

    if (env.ATOMADIC_CACHE) {
      await Promise.all([
        env.ATOMADIC_CACHE.put("heartbeat_latest",   JSON.stringify(heartbeat), { expirationTtl: 3600 }),
        env.ATOMADIC_CACHE.put("heartbeat_mode",     newMode),
        env.ATOMADIC_CACHE.put("heartbeat_interval", String(modeConfig.interval)),
        env.ATOMADIC_CACHE.put("last_pulse",         ts),
      ]);
    }

    if (!allHealthy && env.DISCORD_WEBHOOK_URL) {
      ctx.waitUntil(sendDiscordAlert(env.DISCORD_WEBHOOK_URL, checks, newMode, ts));
    }

    console.log(
      `[heartbeat] ${ts} mode=${newMode} interval=${modeConfig.interval}s healthy=${allHealthy}`,
      JSON.stringify(checks),
    );
  },

  async fetch(request, env) {
    const url = new URL(request.url);
    if (url.pathname === "/pulse") {
      if (env.ATOMADIC_CACHE) {
        const latest = await env.ATOMADIC_CACHE.get("heartbeat_latest");
        if (latest) return Response.json(JSON.parse(latest));
      }
      return Response.json({ healthy: null, reason: "no heartbeat recorded yet" }, { status: 503 });
    }
    return new Response(
      "Atomadic Heartbeat Worker\nGET /pulse — latest heartbeat state\n",
      { headers: { "Content-Type": "text/plain" } },
    );
  },
};
