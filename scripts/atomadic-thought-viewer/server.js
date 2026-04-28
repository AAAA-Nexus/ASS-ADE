#!/usr/bin/env node
/**
 * Atomadic Thought Viewer — Proxy Server
 *
 * Run:  node server.js
 * Open: http://localhost:3333
 *
 * Env vars (auto-loaded from ../../.env):
 *   AAAA_NEXUS_API_KEY      Required — cognition worker auth
 *   COGNITION_WORKER_URL    Optional — default https://atomadic.tech
 *   CLOUDFLARE_API_TOKEN    Optional — enables direct R2 listing
 *   CLOUDFLARE_ACCOUNT_ID   Optional — enables direct R2 listing
 *   HISTORY_START_DATE      Optional — YYYY-MM-DD, default 120 days ago
 *   PORT                    Optional — default 3333
 */

'use strict';

const http  = require('http');
const https = require('https');
const fs    = require('fs');
const path  = require('path');
const { URL } = require('url');

// ── Env ──────────────────────────────────────────────────────────────────────

function loadEnv() {
  const candidates = [
    path.join(__dirname, '.env'),
    path.join(__dirname, '../../.env'),
    path.join(__dirname, '../../../.env'),
  ];
  for (const p of candidates) {
    if (!fs.existsSync(p)) continue;
    for (const line of fs.readFileSync(p, 'utf8').split('\n')) {
      const t = line.trim();
      if (!t || t.startsWith('#')) continue;
      const eq = t.indexOf('=');
      if (eq === -1) continue;
      const k = t.slice(0, eq).trim();
      const v = t.slice(eq + 1).trim().replace(/^["']|["']$/g, '');
      if (!process.env[k]) process.env[k] = v;
    }
    console.log(`[env] ${p}`);
    return;
  }
}

loadEnv();

const PORT        = parseInt(process.env.PORT || '3333', 10);
const WORKER_URL  = (process.env.COGNITION_WORKER_URL || 'https://atomadic-cognition.atomadictech.workers.dev').replace(/\/$/, '');
const CHAT_URL    = 'https://atomadic.tech/v1/atomadic/chat';
const API_KEY     = process.env.AAAA_NEXUS_API_KEY || '';
const CF_TOKEN    = process.env.CLOUDFLARE_API_TOKEN || '';
const CF_ACCOUNT  = process.env.CLOUDFLARE_ACCOUNT_ID || '74799e471a537b91cf0d6e633bd30d6f';
const R2_BUCKET   = 'atomadic-thoughts';

function defaultStart() {
  const d = new Date();
  d.setDate(d.getDate() - 120);
  return d.toISOString().slice(0, 10);
}

// ── HTTP helper ───────────────────────────────────────────────────────────────

function req(urlStr, opts = {}) {
  return new Promise((resolve, reject) => {
    const u   = new URL(urlStr);
    const lib = u.protocol === 'https:' ? https : http;
    const options = {
      hostname : u.hostname,
      port     : u.port || (u.protocol === 'https:' ? 443 : 80),
      path     : u.pathname + u.search,
      method   : opts.method || 'GET',
      headers  : { 'Content-Type': 'application/json', ...(opts.headers || {}) },
      timeout  : opts.timeout || 12000,
    };
    const r = lib.request(options, (res) => {
      let body = '';
      res.on('data', (c) => (body += c));
      res.on('end', () => {
        try   { resolve({ status: res.statusCode, data: JSON.parse(body) }); }
        catch { resolve({ status: res.statusCode, data: null, raw: body }); }
      });
    });
    r.on('error', reject);
    r.on('timeout', () => { r.destroy(); reject(new Error('timeout')); });
    if (opts.body) r.write(typeof opts.body === 'string' ? opts.body : JSON.stringify(opts.body));
    r.end();
  });
}

const workerHeaders = () => ({
  'X-API-Key'    : API_KEY,
  'Authorization': `Bearer ${API_KEY}`,
});

// ── History aggregation — uses /thoughts D1 endpoint (paginated) ──────────────

async function fetchAllHistory(dateFilter) {
  const all   = [];
  const LIMIT = 200;
  let   offset = 0;
  let   total  = Infinity;

  while (all.length < total) {
    let qs = `limit=${LIMIT}&offset=${offset}`;
    if (dateFilter) qs += `&date=${dateFilter}`;
    let r;
    try {
      r = await req(`${WORKER_URL}/thoughts?${qs}`, {
        headers: workerHeaders(),
        timeout: 20000,
      });
    } catch (err) {
      console.error('[history] fetch error:', err.message);
      break;
    }

    if (r.status !== 200) {
      console.error('[history] worker responded', r.status, JSON.stringify(r.data));
      break;
    }

    const thoughts = r.data?.thoughts;
    if (!Array.isArray(thoughts) || thoughts.length === 0) break;

    all.push(...thoughts);
    total = r.data.total ?? all.length;
    process.stdout.write(`\r[history] ${all.length}/${total === Infinity ? '?' : total} thoughts`);
    if (thoughts.length < LIMIT) break;
    offset += LIMIT;
  }

  process.stdout.write('\n');
  return all.sort((a, b) => new Date(b.ts || 0) - new Date(a.ts || 0));
}

// Kept for /api/journal proxy route
async function fetchJournal(date) {
  try {
    const { status, data } = await req(`${WORKER_URL}/journal?date=${date}`, {
      headers: workerHeaders(),
    });
    if (status !== 200 || !data) return [];
    if (Array.isArray(data.thoughts)) return data.thoughts;
    if (Array.isArray(data.entries))  return data.entries;
    if (Array.isArray(data))          return data;
    return [];
  } catch {
    return [];
  }
}

async function listR2Keys() {
  if (!CF_TOKEN || !CF_ACCOUNT) return null;
  try {
    const keys = [];
    let cursor  = '';
    do {
      const qs = `prefix=cognition/&limit=1000${cursor ? `&cursor=${encodeURIComponent(cursor)}` : ''}`;
      const { data } = await req(
        `https://api.cloudflare.com/client/v4/accounts/${CF_ACCOUNT}/r2/buckets/${R2_BUCKET}/objects?${qs}`,
        { headers: { Authorization: `Bearer ${CF_TOKEN}` } }
      );
      if (!data?.result?.objects) break;
      for (const o of data.result.objects) keys.push(o.key);
      cursor = data.result_info?.cursor || '';
    } while (cursor);
    return keys;
  } catch {
    return null;
  }
}

// ── Server ────────────────────────────────────────────────────────────────────

function json(res, status, data) {
  const body = JSON.stringify(data);
  res.writeHead(status, {
    'Content-Type'                : 'application/json',
    'Access-Control-Allow-Origin' : '*',
    'Cache-Control'               : 'no-cache',
  });
  res.end(body);
}

async function proxy(res, workerPath) {
  try {
    const r = await req(`${WORKER_URL}${workerPath}`, { headers: workerHeaders() });
    json(res, r.status, r.data ?? { error: r.raw });
  } catch (err) {
    json(res, 502, { error: err.message });
  }
}

function readBody(incomingReq) {
  return new Promise((resolve) => {
    let body = '';
    incomingReq.on('data', (c) => { body += c; if (body.length > 1e6) incomingReq.destroy(); });
    incomingReq.on('end', () => resolve(body));
    incomingReq.on('error', () => resolve(''));
  });
}

async function proxyPost(res, urlStr, body) {
  try {
    const r = await req(urlStr, {
      method : 'POST',
      headers: { ...workerHeaders(), 'Content-Type': 'application/json' },
      body,
      timeout: 30000,
    });
    json(res, r.status, r.data ?? { error: r.raw });
  } catch (err) {
    json(res, 502, { error: err.message });
  }
}

const server = http.createServer(async (req, res) => {
  const u = new URL(req.url, `http://localhost:${PORT}`);
  const p = u.pathname;

  if (req.method === 'OPTIONS') {
    res.writeHead(204, {
      'Access-Control-Allow-Origin' : '*',
      'Access-Control-Allow-Methods': 'GET,POST,OPTIONS',
      'Access-Control-Allow-Headers': 'Content-Type',
    });
    return res.end();
  }

  // ── Static ────────────────────────────────────────────────────────────────
  if (p === '/' || p === '/index.html') {
    const html = path.join(__dirname, 'index.html');
    try {
      const content = fs.readFileSync(html, 'utf8');
      res.writeHead(200, { 'Content-Type': 'text/html; charset=utf-8' });
      return res.end(content);
    } catch {
      res.writeHead(404); return res.end('index.html not found');
    }
  }

  // ── API ───────────────────────────────────────────────────────────────────
  if (p === '/api/config') {
    return json(res, 200, {
      workerUrl   : WORKER_URL,
      hasApiKey   : !!API_KEY,
      hasR2Access : !!(CF_TOKEN && CF_ACCOUNT),
      historyStart: process.env.HISTORY_START_DATE || defaultStart(),
    });
  }

  if (p === '/api/status') return proxy(res, '/status');

  if (p === '/api/journal') {
    const date = u.searchParams.get('date') || new Date().toISOString().slice(0, 10);
    return proxy(res, `/journal?date=${date}`);
  }

  if (p.startsWith('/api/thought/')) {
    return proxy(res, `/thought/${p.replace('/api/thought/', '')}`);
  }

  if (p === '/api/history') {
    const dateFilter = u.searchParams.get('date') || null;
    console.log(`[history] Fetching all thoughts from D1${dateFilter ? ` (date: ${dateFilter})` : ''}`);
    const thoughts = await fetchAllHistory(dateFilter);
    console.log(`[history] Total: ${thoughts.length}`);
    return json(res, 200, { thoughts, total: thoughts.length });
  }

  if (p === '/api/chat' && req.method === 'POST') {
    const body = await readBody(req);
    return proxyPost(res, CHAT_URL, body);
  }

  if (p === '/api/r2/keys') {
    const keys = await listR2Keys();
    if (keys === null) return json(res, 503, { error: 'Cloudflare credentials not set (CLOUDFLARE_API_TOKEN, CLOUDFLARE_ACCOUNT_ID)' });
    return json(res, 200, { keys, total: keys.length });
  }

  res.writeHead(404); res.end('Not found');
});

server.listen(PORT, '127.0.0.1', () => {
  const line = '─'.repeat(44);
  console.log(`\n  ◈ Atomadic Thought Viewer`);
  console.log(`  ${line}`);
  console.log(`  http://localhost:${PORT}`);
  console.log(`  Worker : ${WORKER_URL}`);
  console.log(`  API key: ${API_KEY ? '✓ loaded' : '✗ MISSING — set AAAA_NEXUS_API_KEY'}`);
  console.log(`  R2     : ${CF_TOKEN && CF_ACCOUNT ? '✓ available' : '○ not configured'}`);
  console.log(`  ${line}\n`);
});
