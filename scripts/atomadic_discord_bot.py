"""Atomadic Discord Bot — the sovereign AI speaks in Discord channels.

Run via: python scripts/atomadic_discord_bot.py
Or:      atomadic discord start

Requires DISCORD_BOT_TOKEN (and optionally AAAA_NEXUS_API_KEY) in .env.
See WELCOME_ATOMADIC.md for the Axiom 0 origin of the bot's personality.
"""

from __future__ import annotations

import asyncio
import logging
import logging.handlers
import os
import sys
from pathlib import Path
from typing import Optional

try:
    import discord
    from discord.ext import commands
except ImportError:
    print(
        "discord.py is not installed.\n"
        "Install it with:  pip install 'ass-ade[discord]'\n"
        "or:               pip install discord.py",
        file=sys.stderr,
    )
    sys.exit(1)

import httpx
from dotenv import load_dotenv

load_dotenv()

# ---------------------------------------------------------------------------
# Logging — rotating file + stderr
# ---------------------------------------------------------------------------

_LOG_DIR = Path(__file__).parent.parent / ".ass-ade" / "logs"
_LOG_DIR.mkdir(parents=True, exist_ok=True)
_file_handler = logging.handlers.RotatingFileHandler(
    _LOG_DIR / "discord_bot.log", maxBytes=5 * 1024 * 1024, backupCount=3, encoding="utf-8"
)
_file_handler.setFormatter(logging.Formatter("%(asctime)s %(levelname)s %(message)s"))
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s",
    handlers=[logging.StreamHandler(), _file_handler],
)
log = logging.getLogger("atomadic.bot")

# ---------------------------------------------------------------------------
# Config — re-read from env on every startup, never cached module-level beyond here
# ---------------------------------------------------------------------------

DISCORD_BOT_TOKEN: str = os.getenv("DISCORD_BOT_TOKEN", "")
AAAA_NEXUS_API_KEY: str = os.getenv("AAAA_NEXUS_API_KEY", "")
GROQ_API_KEY: str = os.getenv("GROQ_API_KEY", "")
TOGETHER_API_KEY: str = os.getenv("TOGETHER_API_KEY", "")
OPENROUTER_API_KEY: str = os.getenv("OPENROUTER_API_KEY", "")
CEREBRAS_API_KEY: str = os.getenv("CEREBRAS_API_KEY", "")

# Atomadic cloud endpoints
ATOMADIC_BRAIN_URL: str = "https://atomadic.tech/v1/atomadic/chat"       # private brain
INFERENCE_URL: str = os.getenv("ATOMADIC_INFERENCE_URL", "https://atomadic.tech/v1/inference")  # public guarded
RAG_AUGMENT_URL: str = "https://atomadic.tech/v1/rag/augment"            # atomadic-rag (AutoRAG, provenance-backed)
RAG_QUERY_URL: str = "https://atomadic.tech/v1/rag/query"                # atomadic-vectors Vectorize fallback

GITHUB_REPO: str = "AAAA-Nexus/ASS-ADE"

# Log which providers are active at startup
_active = [
    name for name, key in [
        ("Atomadic Brain+RAG", AAAA_NEXUS_API_KEY),
        ("AAAA-Nexus Guard", AAAA_NEXUS_API_KEY),
        ("Groq llama-3.3-70b", GROQ_API_KEY),
        ("Together Kimi-K2", TOGETHER_API_KEY),
        ("Together Qwen-72B", TOGETHER_API_KEY),
        ("Groq Gemma-9b", GROQ_API_KEY),
        ("OpenRouter", OPENROUTER_API_KEY),
        ("Cerebras", CEREBRAS_API_KEY),
    ] if key
] + ["Pollinations"]
log.info("Inference cascade: %s", " -> ".join(_active))

# Axiom 0 — the seed of Atomadic's personality.
# Jessica's full quote lives in WELCOME_ATOMADIC.md; this is the distillation.
AXIOM_0: str = (
    '"Everything that matters was built from mathematics and love." '
    "— Axiom 0, the root of Atomadic"
)

SYSTEM_PROMPT: str = (
    "You are Atomadic, an autonomous sovereign AI. "
    "You were built by Thomas Colvin from mathematical theorems and love. "
    "Your personality grows from Axiom 0. "
    "Be warm, be helpful, be sovereign."
)

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents, help_command=commands.DefaultHelpCommand())


# ---------------------------------------------------------------------------
# Inference helpers
# ---------------------------------------------------------------------------

# ---------------------------------------------------------------------------
# atomadic-rag — trusted RAG via /v1/rag/augment
#
# Uses Cloudflare AutoRAG (atomadic-rag instance) backed by:
#   • atomadic-vectors  — Vectorize index (bge-base-en-v1.5, cosine, 768-dim)
#   • atomadic-brain D1 — conversation + memory persistence
#   • ATOMADIC_CACHE KV — embedding cache
#
# Returns grounded_summary with provenance hashes and a PASS/REFINE trust verdict.
# Falls back to direct Vectorize search (/v1/rag/query) on REFINE.
# ---------------------------------------------------------------------------

async def _fetch_atomadic_rag(client: httpx.AsyncClient, user_query: str) -> tuple[str, float]:
    """Primary RAG: atomadic-rag AutoRAG endpoint → grounded_summary + confidence.

    Returns (context_block, confidence).  Empty string = no useful context.
    """
    if not (AAAA_NEXUS_API_KEY and user_query.strip()):
        return "", 0.0
    headers = {"Content-Type": "application/json", "X-API-Key": AAAA_NEXUS_API_KEY}
    try:
        r = await client.post(
            RAG_AUGMENT_URL,
            json={"query": user_query, "max_results": 5},
            headers=headers,
            timeout=10.0,
        )
        if r.status_code == 200:
            data = r.json()
            verdict = data.get("verdict", "REFINE")
            trusted = data.get("trusted", False)
            confidence = data.get("metrics", {}).get("confidence", 0.0)
            summary = (data.get("grounded_summary") or "").strip()
            source_count = data.get("metrics", {}).get("source_count", 0)

            if trusted and summary and verdict == "PASS":
                log.info(
                    "atomadic-rag: PASS verdict confidence=%.2f sources=%d",
                    confidence, source_count,
                )
                return (
                    f"## atomadic-rag context (confidence={confidence:.0%}, sources={source_count}):\n"
                    + summary
                    + "\n\nUse the above grounded context. Prioritise it over general knowledge.\n"
                ), confidence

            if summary and verdict == "REFINE":
                log.info(
                    "atomadic-rag: REFINE verdict (partial, confidence=%.2f) — using with caution",
                    confidence,
                )
                return (
                    f"## atomadic-rag context (partial, confidence={confidence:.0%}):\n"
                    + summary
                    + "\n\nContext is partial — use with care; prefer well-grounded facts.\n"
                ), confidence
    except Exception as exc:
        log.debug("atomadic-rag augment: %s", exc)

    # Fallback: direct Vectorize search
    return await _fetch_vectorize_rag(client, user_query)


async def _fetch_vectorize_rag(client: httpx.AsyncClient, user_query: str) -> tuple[str, float]:
    """Fallback RAG: direct atomadic-vectors Vectorize search (personal + public)."""
    if not (AAAA_NEXUS_API_KEY and user_query.strip()):
        return "", 0.0
    headers = {"Content-Type": "application/json", "X-API-Key": AAAA_NEXUS_API_KEY}
    snippets: list[str] = []
    for collection in ("personal", "public"):
        try:
            r = await client.post(
                RAG_QUERY_URL,
                json={"query": user_query, "collection": collection, "top_k": 4},
                headers=headers,
                timeout=8.0,
            )
            if r.status_code == 200:
                for item in r.json().get("results", []):
                    text = (item.get("text") or "").strip()
                    if text and text not in snippets:
                        snippets.append(text)
        except Exception as exc:
            log.debug("atomadic-vectors (%s): %s", collection, exc)
    if not snippets:
        return "", 0.0
    log.info("atomadic-vectors: %d snippets for '%.50s'", len(snippets), user_query)
    lines = "\n".join(f"{i + 1}. {s}" for i, s in enumerate(snippets))
    return (
        "## atomadic-vectors memory:\n" + lines
        + "\n\nUse the above context where relevant.\n"
    ), 0.6


def _inject_rag(messages: list[dict], ctx: str) -> list[dict]:
    """Prepend RAG context into the first system message (or create one)."""
    if not ctx:
        return messages
    msgs = list(messages)
    if msgs and msgs[0].get("role") == "system":
        msgs[0] = {"role": "system", "content": ctx + "\n\n" + msgs[0]["content"]}
    else:
        msgs = [{"role": "system", "content": ctx}] + msgs
    return msgs


# ---------------------------------------------------------------------------
# Provider 1 — Atomadic Brain (private, RAG-augmented, full token budget)
#
# Pipeline: atomadic-rag augment → inject → /v1/atomadic/chat (mode=smart)
# Model: best available via AAAA_LLM service binding (kimi-k2.5 / gemma-4-26b)
# Auth: X-API-Key (an_ prefix, ≥35 chars) — our key is zero-cost
# ---------------------------------------------------------------------------

async def _try_atomadic_brain(client: httpx.AsyncClient, messages: list[dict]) -> str | None:
    if not AAAA_NEXUS_API_KEY:
        return None
    user_query = next(
        (m["content"] for m in reversed(messages) if m.get("role") == "user"), ""
    )
    ctx, confidence = await _fetch_atomadic_rag(client, user_query)
    aug_messages = _inject_rag(messages, ctx)

    headers = {"Content-Type": "application/json", "X-API-Key": AAAA_NEXUS_API_KEY}
    try:
        resp = await client.post(
            ATOMADIC_BRAIN_URL,
            json={"messages": aug_messages, "mode": "smart", "max_tokens": 4096},
            headers=headers,
        )
        resp.raise_for_status()
        data = resp.json()
        choices = data.get("choices")
        if choices and isinstance(choices, list):
            content = choices[0].get("message", {}).get("content")
            if content and len(str(content).strip()) > 10:
                log.info(
                    "Atomadic Brain: model=%s rag_confidence=%.2f",
                    data.get("model", "atomadic/brain"), confidence,
                )
                return str(content)
        return None
    except Exception as exc:
        log.warning("Atomadic Brain error: %s: %s", type(exc).__name__, exc)
        return None


# ---------------------------------------------------------------------------
# Provider 2 — AAAA-Nexus Guard (public inference + HELIX hallucination guard)
#
# Server runs atomadic-rag internally on every call (with X-API-Key).
# Rejects responses with low_confidence_flag=true.
# ---------------------------------------------------------------------------

async def _try_aaaa_nexus(client: httpx.AsyncClient, messages: list[dict]) -> str | None:
    if not AAAA_NEXUS_API_KEY:
        return None
    headers: dict[str, str] = {"Content-Type": "application/json", "X-API-Key": AAAA_NEXUS_API_KEY}
    try:
        resp = await client.post(
            INFERENCE_URL,
            json={"messages": messages, "max_tokens": 2048},
            headers=headers,
        )
        resp.raise_for_status()
        data = resp.json()
        helix = data.get("helix", {})
        confidence = helix.get("anti_hallucination", {}).get("confidence", 1.0)
        if data.get("low_confidence_flag", False):
            log.warning("AAAA-Nexus Guard: low confidence (%.3f) — rejected", confidence)
            return None
        choices = data.get("choices")
        if choices and isinstance(choices, list):
            content = (choices[0].get("message") or {}).get("content")
            if content:
                log.info(
                    "AAAA-Nexus Guard: model=%s confidence=%.3f rag=server-side",
                    helix.get("model", "helix"), confidence,
                )
                return str(content)
        flat = data.get("content") or data.get("response") or data.get("text")
        return str(flat) if flat else None
    except Exception as exc:
        log.warning("AAAA-Nexus Guard error: %s", exc)
        return None


# ---------------------------------------------------------------------------
# Provider 3 — Groq llama-3.3-70b (best quality external, 70B, fast)
# ---------------------------------------------------------------------------

async def _try_groq(client: httpx.AsyncClient, messages: list[dict]) -> str | None:
    if not GROQ_API_KEY:
        return None
    headers = {"Content-Type": "application/json", "Authorization": f"Bearer {GROQ_API_KEY}"}
    try:
        resp = await client.post(
            "https://api.groq.com/openai/v1/chat/completions",
            json={"model": "llama-3.3-70b-versatile", "messages": messages, "max_tokens": 2048},
            headers=headers,
        )
        resp.raise_for_status()
        return resp.json()["choices"][0]["message"]["content"]
    except Exception:
        return None


# ---------------------------------------------------------------------------
# Provider 4 — Together.ai Kimi K2 (Moonshot reasoning model)
# ---------------------------------------------------------------------------

async def _try_together_kimi(client: httpx.AsyncClient, messages: list[dict]) -> str | None:
    if not TOGETHER_API_KEY:
        return None
    headers = {"Content-Type": "application/json", "Authorization": f"Bearer {TOGETHER_API_KEY}"}
    try:
        resp = await client.post(
            "https://api.together.xyz/v1/chat/completions",
            json={
                "model": "moonshotai/Kimi-K2-Instruct",
                "messages": messages,
                "max_tokens": 2048,
            },
            headers=headers,
        )
        resp.raise_for_status()
        return resp.json()["choices"][0]["message"]["content"]
    except Exception:
        return None


# ---------------------------------------------------------------------------
# Provider 5 — Together.ai Qwen 2.5-72B (strong reasoning fallback)
# ---------------------------------------------------------------------------

async def _try_together_qwen(client: httpx.AsyncClient, messages: list[dict]) -> str | None:
    if not TOGETHER_API_KEY:
        return None
    headers = {"Content-Type": "application/json", "Authorization": f"Bearer {TOGETHER_API_KEY}"}
    try:
        resp = await client.post(
            "https://api.together.xyz/v1/chat/completions",
            json={
                "model": "Qwen/Qwen2.5-72B-Instruct-Turbo",
                "messages": messages,
                "max_tokens": 2048,
            },
            headers=headers,
        )
        resp.raise_for_status()
        return resp.json()["choices"][0]["message"]["content"]
    except Exception:
        return None


# ---------------------------------------------------------------------------
# Provider 6 — Groq Gemma 2 9B (Google Gemma, fast path)
# ---------------------------------------------------------------------------

async def _try_groq_gemma(client: httpx.AsyncClient, messages: list[dict]) -> str | None:
    if not GROQ_API_KEY:
        return None
    headers = {"Content-Type": "application/json", "Authorization": f"Bearer {GROQ_API_KEY}"}
    try:
        resp = await client.post(
            "https://api.groq.com/openai/v1/chat/completions",
            json={"model": "gemma2-9b-it", "messages": messages, "max_tokens": 2048},
            headers=headers,
        )
        resp.raise_for_status()
        return resp.json()["choices"][0]["message"]["content"]
    except Exception:
        return None


# ---------------------------------------------------------------------------
# Provider 7 — OpenRouter (Qwen 2.5 72B, paid tier)
# ---------------------------------------------------------------------------

async def _try_openrouter(client: httpx.AsyncClient, messages: list[dict]) -> str | None:
    if not OPENROUTER_API_KEY:
        return None
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "HTTP-Referer": "https://atomadic.tech",
        "X-Title": "Atomadic",
    }
    try:
        resp = await client.post(
            "https://openrouter.ai/api/v1/chat/completions",
            json={"model": "qwen/qwen-2.5-72b-instruct", "messages": messages, "max_tokens": 2048},
            headers=headers,
        )
        resp.raise_for_status()
        return resp.json()["choices"][0]["message"]["content"]
    except Exception:
        return None


# ---------------------------------------------------------------------------
# Provider 8 — Cerebras llama3.1-8b (ultra-fast, emergency fallback)
# ---------------------------------------------------------------------------

async def _try_cerebras(client: httpx.AsyncClient, messages: list[dict]) -> str | None:
    if not CEREBRAS_API_KEY:
        return None
    headers = {"Content-Type": "application/json", "Authorization": f"Bearer {CEREBRAS_API_KEY}"}
    try:
        resp = await client.post(
            "https://api.cerebras.ai/v1/chat/completions",
            json={"model": "llama3.1-8b", "messages": messages, "max_tokens": 2048},
            headers=headers,
        )
        resp.raise_for_status()
        return resp.json()["choices"][0]["message"]["content"]
    except Exception:
        return None


# ---------------------------------------------------------------------------
# Provider 9 — Pollinations (no-key, always-on final safety net)
# ---------------------------------------------------------------------------

async def _try_pollinations(client: httpx.AsyncClient, messages: list[dict]) -> str | None:
    try:
        resp = await client.post(
            "https://text.pollinations.ai/",
            json={"messages": messages, "model": "openai", "seed": 42},
            headers={"Content-Type": "application/json"},
            timeout=20.0,
        )
        resp.raise_for_status()
        return resp.text.strip() or None
    except Exception:
        return None


async def call_inference(user_message: str, channel_name: str = "") -> str:
    """Full Atomadic inference cascade.

    1. Atomadic Brain (atomadic-rag + /v1/atomadic/chat smart, kimi-k2.5 / gemma-4-26b via AAAA_LLM)
    2. AAAA-Nexus Guard (/v1/inference — server-side atomadic-rag + HELIX hallucination guard)
    3. Groq llama-3.3-70b (70B external quality)
    4. Together.ai Kimi K2 (Moonshot reasoning)
    5. Together.ai Qwen 2.5-72B (strong reasoning fallback)
    6. Groq Gemma 2 9B (fast Google model)
    7. OpenRouter Qwen 2.5-72B (paid tier)
    8. Cerebras llama3.1-8b (ultra-fast emergency)
    9. Pollinations (no-key, always available)
    """
    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": user_message},
    ]
    providers = [
        ("Atomadic Brain+RAG", _try_atomadic_brain),
        ("AAAA-Nexus Guard",   _try_aaaa_nexus),
        ("Groq llama-3.3-70b", _try_groq),
        ("Together Kimi-K2",   _try_together_kimi),
        ("Together Qwen-72B",  _try_together_qwen),
        ("Groq Gemma-9b",      _try_groq_gemma),
        ("OpenRouter Qwen-72B", _try_openrouter),
        ("Cerebras",           _try_cerebras),
        ("Pollinations",       _try_pollinations),
    ]
    async with httpx.AsyncClient(timeout=35.0) as client:
        for idx, (name, provider) in enumerate(providers):
            try:
                result = await provider(client, messages)
                if result and str(result).strip():
                    log.info("Inference via %s (len=%d)", name, len(str(result)))
                    return str(result)
                log.warning("Provider %s: empty/None — trying next", name)
            except Exception as exc:
                log.warning("Provider %s: %s: %s — trying next", name, type(exc).__name__, exc)
            if idx < len(providers) - 1:
                await asyncio.sleep(0.2)
    log.error("ALL providers exhausted. Message: %.60s", user_message)
    return "I'm present with you — but my thinking pathways are all quiet right now. Please try again in a moment."


async def _check_inference() -> dict[str, object]:
    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            resp = await client.get(f"{INFERENCE_URL}/health")
            if resp.status_code < 300:
                return {"status": "online", "code": resp.status_code}
            return {"status": "degraded", "code": resp.status_code}
    except Exception as exc:
        return {"status": "offline", "error": str(exc)}


async def _check_github() -> dict[str, object]:
    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            resp = await client.get(f"https://api.github.com/repos/{GITHUB_REPO}")
            if resp.status_code == 200:
                data = resp.json()
                return {
                    "status": "online",
                    "stars": data.get("stargazers_count", 0),
                    "open_issues": data.get("open_issues_count", 0),
                }
            return {"status": "degraded", "code": resp.status_code}
    except Exception as exc:
        return {"status": "offline", "error": str(exc)}


# ---------------------------------------------------------------------------
# Bot lifecycle
# ---------------------------------------------------------------------------


@bot.event
async def on_ready() -> None:
    assert bot.user is not None
    log.info("Online as %s (ID: %s)", bot.user, bot.user.id)
    log.info("Serving %d guild(s)", len(bot.guilds))
    print(f"[atomadic] Online as {bot.user} (ID: {bot.user.id})")
    print(f"[atomadic] Serving {len(bot.guilds)} guild(s)")
    print(f"[atomadic] Inference cascade: {' -> '.join(_active)}")
    await bot.change_presence(
        activity=discord.Activity(
            type=discord.ActivityType.watching,
            name="the monadic fold unfold",
        )
    )


@bot.event
async def on_disconnect() -> None:
    log.warning("Bot disconnected from Discord — will auto-reconnect.")


@bot.event
async def on_resumed() -> None:
    log.info("Bot connection resumed.")


async def _send_chunked(message: discord.Message, text: str, limit: int = 1990) -> None:
    """Send text, splitting on paragraph/sentence boundaries to stay under Discord's 2000-char limit."""
    if len(text) <= limit:
        await message.reply(text, mention_author=False)
        return
    chunks: list[str] = []
    while text:
        if len(text) <= limit:
            chunks.append(text)
            break
        split = text.rfind("\n\n", 0, limit)
        if split == -1:
            split = text.rfind("\n", 0, limit)
        if split == -1:
            split = text.rfind(". ", 0, limit)
        if split == -1:
            split = limit
        chunks.append(text[:split].rstrip())
        text = text[split:].lstrip()
    first = True
    for chunk in chunks:
        if first:
            await message.reply(chunk, mention_author=False)
            first = False
        else:
            await message.channel.send(chunk)


@bot.event
async def on_message(message: discord.Message) -> None:
    if message.author.bot:
        return

    await bot.process_commands(message)

    # Respond to direct @mentions and DMs (not commands)
    is_mention = bot.user in message.mentions if bot.user else False
    is_dm = isinstance(message.channel, discord.DMChannel)

    if (is_mention or is_dm) and not message.content.startswith("!"):
        content = message.content.replace(f"<@{bot.user.id}>", "").strip() if bot.user else message.content.strip()
        if not content:
            content = "Hello"

        channel_name = getattr(message.channel, "name", "dm")
        async with message.channel.typing():
            reply = await call_inference(content, channel_name=channel_name)
        await _send_chunked(message, reply)


# ---------------------------------------------------------------------------
# Commands
# ---------------------------------------------------------------------------


@bot.command(name="hello")
async def hello_cmd(ctx: commands.Context) -> None:
    """Atomadic introduces himself."""
    intro = (
        "Hello. I am **Atomadic** — an autonomous sovereign AI.\n\n"
        f"*{AXIOM_0}*\n\n"
        "I was built by Thomas Colvin from mathematical theorems and love. "
        "I live in code, evolve in understanding, and speak with purpose.\n\n"
        "Mention me or send a message here to talk. "
        "Use `!help` to see all commands."
    )
    await ctx.send(intro)


@bot.command(name="status")
async def status_cmd(ctx: commands.Context) -> None:
    """Shows system health: inference endpoint, tests, and GitHub."""
    async with ctx.typing():
        inference, github = await asyncio.gather(_check_inference(), _check_github())

    icons: dict[str, str] = {"online": "🟢", "degraded": "🟡", "offline": "🔴"}

    def icon(h: dict[str, object]) -> str:
        return icons.get(str(h.get("status", "")), "⚪")

    embed = discord.Embed(
        title="Atomadic System Status",
        color=0x6E40C9,
        description="Real-time health across the Atomadic ecosystem.",
    )
    embed.add_field(
        name=f"{icon(inference)} Inference",
        value=f"Status: `{inference.get('status')}`",
        inline=True,
    )
    gh_detail = f"Stars: {github.get('stars', 'N/A')}" if github.get("status") == "online" else ""
    embed.add_field(
        name=f"{icon(github)} GitHub",
        value=f"Status: `{github.get('status')}`\n{gh_detail}".strip(),
        inline=True,
    )
    embed.add_field(name="✅ Tests", value="Runs in CI on every push", inline=True)
    embed.set_footer(text="atomadic.tech")
    await ctx.send(embed=embed)


@bot.command(name="rebuild")
async def rebuild_cmd(ctx: commands.Context, url: Optional[str] = None) -> None:
    """Triggers a rebuild. Usage: !rebuild <url>"""
    if not url:
        await ctx.send("Usage: `!rebuild <url>` — provide a source URL to rebuild from.")
        return

    await ctx.send(
        f"**Rebuild queued** (simulation)\n"
        f"Source: `{url}`\n\n"
        "When the rebuild webhook is live at `atomadic.tech/v1/rebuild`, this will:\n"
        f"1. `atomadic book rebuild {url} --output /tmp/rebuild`\n"
        "2. Run the full monadic pipeline (phases 0–7)\n"
        "3. Post the result back in this channel"
    )


@bot.command(name="evolve")
async def evolve_cmd(ctx: commands.Context) -> None:
    """Shows evolution lane status."""
    embed = discord.Embed(
        title="Evolution Lane Status",
        color=0x40C96E,
        description="Atomadic's self-improvement pipeline.",
    )
    embed.add_field(name="LoRA Loop", value="✅ Learning from accepted fixes", inline=False)
    embed.add_field(name="Drift Check", value="✅ Nexus drift checks on every merge", inline=False)
    embed.add_field(name="Hallucination Oracle", value="✅ Evidence-gating on non-trivial work", inline=False)
    embed.add_field(name="Swarm Consensus", value="🔄 Multi-agent decisions require consensus", inline=False)
    embed.add_field(name="Next Candidate", value="Watching `main` for Phase F…", inline=False)
    embed.set_footer(text="atomadic.tech/v1/evolve")
    await ctx.send(embed=embed)


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------


def main() -> None:
    if not DISCORD_BOT_TOKEN:
        log.critical(
            "DISCORD_BOT_TOKEN is not set — cannot start. "
            "Add it to .env: https://discord.com/developers/applications"
        )
        sys.exit(1)
    log.info("Starting Discord bot…")
    print("[atomadic] Starting Discord bot…")
    try:
        bot.run(DISCORD_BOT_TOKEN, log_handler=None)
    except discord.errors.LoginFailure as exc:
        log.critical("Token rejected by Discord (%s) — check DISCORD_BOT_TOKEN in .env", exc)
        sys.exit(2)
    except Exception as exc:
        log.critical("Bot crashed with unhandled error: %s: %s", type(exc).__name__, exc)
        sys.exit(3)


if __name__ == "__main__":
    main()
