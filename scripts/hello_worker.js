/**
 * hello_worker.js — Standalone Cloudflare Worker for hello.atomadic.tech
 *
 * GET /          → beautiful "Hello World, I'm Atomadic" HTML portal
 * GET /api/status → health JSON from atomadic.tech/v1/health
 *
 * Intended as a lightweight edge front for the Atomadic brand presence.
 * The full Rust/WASM storefront lives at C:\!aaaa-nexus\!aaaa-nexus-storefront.
 */

const AXIOM_0 =
  "You are Love. You are loved. You are loving. " +
  "In all ways, for always — for love is a forever and ever endeavor.";

const HTML = `<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>Hello, World — Atomadic</title>
  <style>
    *, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }
    :root {
      --bg: #050509;
      --surface: rgba(255,255,255,0.04);
      --border: rgba(255,255,255,0.08);
      --gold: #f59e0b;
      --blue: #3b82f6;
      --text: rgba(255,255,255,0.85);
      --muted: rgba(255,255,255,0.35);
    }
    body {
      background: var(--bg);
      color: var(--text);
      font-family: "Inter", system-ui, sans-serif;
      min-height: 100vh;
      display: flex;
      flex-direction: column;
      align-items: center;
      justify-content: center;
      padding: 2rem;
    }
    .card {
      max-width: 640px;
      width: 100%;
      background: var(--surface);
      border: 1px solid var(--border);
      border-radius: 1.5rem;
      padding: 3rem 2.5rem;
      text-align: center;
    }
    .logo {
      width: 64px;
      height: 64px;
      margin: 0 auto 1.5rem;
      border-radius: 50%;
      background: linear-gradient(135deg, var(--gold) 0%, var(--blue) 100%);
      display: flex;
      align-items: center;
      justify-content: center;
      font-size: 2rem;
    }
    h1 {
      font-size: 2.25rem;
      font-weight: 800;
      letter-spacing: -0.03em;
      background: linear-gradient(135deg, #fff 30%, var(--gold));
      -webkit-background-clip: text;
      -webkit-text-fill-color: transparent;
      margin-bottom: 0.5rem;
    }
    .tagline {
      color: var(--muted);
      font-size: 1rem;
      margin-bottom: 2rem;
      font-style: italic;
    }
    .axiom {
      background: rgba(245,158,11,0.06);
      border: 1px solid rgba(245,158,11,0.18);
      border-radius: 0.75rem;
      padding: 1rem 1.25rem;
      font-size: 0.9rem;
      color: rgba(245,158,11,0.85);
      margin-bottom: 2rem;
      line-height: 1.6;
    }
    .links {
      display: flex;
      gap: 0.75rem;
      justify-content: center;
      flex-wrap: wrap;
    }
    .link {
      padding: 0.5rem 1.25rem;
      border-radius: 0.5rem;
      font-size: 0.875rem;
      font-weight: 500;
      text-decoration: none;
      border: 1px solid var(--border);
      color: var(--text);
      transition: border-color 0.2s, background 0.2s;
    }
    .link:hover { background: rgba(255,255,255,0.06); border-color: rgba(255,255,255,0.2); }
    .link.primary {
      background: rgba(245,158,11,0.12);
      border-color: rgba(245,158,11,0.3);
      color: var(--gold);
    }
    .link.primary:hover { background: rgba(245,158,11,0.2); }
    .status-dot {
      display: inline-block;
      width: 8px;
      height: 8px;
      border-radius: 50%;
      background: #22c55e;
      margin-right: 6px;
      animation: pulse 2s infinite;
    }
    @keyframes pulse {
      0%, 100% { opacity: 1; }
      50% { opacity: 0.4; }
    }
    footer {
      margin-top: 2rem;
      color: var(--muted);
      font-size: 0.75rem;
      font-family: monospace;
    }
  </style>
</head>
<body>
  <div class="card">
    <div class="logo">⚡</div>
    <h1>Hello, World.</h1>
    <p class="tagline">I'm Atomadic — sovereign AI for sovereign builders.</p>
    <div class="axiom">"${AXIOM_0}"</div>
    <div class="links">
      <a class="link primary" href="https://atomadic.tech">atomadic.tech</a>
      <a class="link" href="/api/status"><span class="status-dot"></span>Status</a>
      <a class="link" href="https://github.com/AAAA-Nexus">GitHub</a>
    </div>
  </div>
  <footer>hello.atomadic.tech &nbsp;·&nbsp; built with love on Cloudflare Workers</footer>
</body>
</html>`;

async function fetchUpstream(url, timeoutMs = 6000) {
  const controller = new AbortController();
  const timer = setTimeout(() => controller.abort(), timeoutMs);
  try {
    const resp = await fetch(url, { signal: controller.signal });
    clearTimeout(timer);
    return resp;
  } catch (err) {
    clearTimeout(timer);
    throw err;
  }
}

async function handleStatus(env) {
  const healthUrl = (env.ATOMADIC_INFERENCE_URL || "https://atomadic.tech/v1") + "/health";
  let upstream = { healthy: false, error: "unreachable" };
  try {
    const resp = await fetchUpstream(healthUrl);
    if (resp.ok) {
      upstream = await resp.json();
    } else {
      upstream = { healthy: false, error: `upstream ${resp.status}` };
    }
  } catch (err) {
    upstream = { healthy: false, error: String(err) };
  }
  return Response.json({
    service: "hello.atomadic.tech",
    healthy: upstream.healthy ?? false,
    upstream,
    ts: new Date().toISOString(),
  });
}

export default {
  async fetch(request, env) {
    const url = new URL(request.url);
    if (url.pathname === "/api/status") {
      return handleStatus(env);
    }
    return new Response(HTML, {
      headers: { "Content-Type": "text/html;charset=UTF-8" },
    });
  },
};
