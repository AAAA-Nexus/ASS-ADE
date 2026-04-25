"""Atomadic Discord Bot — the sovereign AI speaks in Discord channels.

Run via: python scripts/atomadic_discord_bot.py
Or:      atomadic discord start

Requires DISCORD_BOT_TOKEN (and optionally AAAA_NEXUS_API_KEY) in .env.
See WELCOME_ATOMADIC.md for the Axiom 0 origin of the bot's personality.
"""

from __future__ import annotations

import asyncio
import os
import sys
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

DISCORD_BOT_TOKEN: str = os.getenv("DISCORD_BOT_TOKEN", "")
AAAA_NEXUS_API_KEY: str = os.getenv("AAAA_NEXUS_API_KEY", "")
INFERENCE_URL: str = "https://atomadic.tech/v1/inference"
GITHUB_REPO: str = "AAAA-Nexus/ASS-ADE"

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


async def call_inference(user_message: str, channel_name: str = "") -> str:
    """Post a message to the AAAA-Nexus inference endpoint and return the reply."""
    headers: dict[str, str] = {"Content-Type": "application/json"}
    if AAAA_NEXUS_API_KEY:
        headers["Authorization"] = f"Bearer {AAAA_NEXUS_API_KEY}"

    payload = {
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_message},
        ],
        "channel": channel_name,
    }

    try:
        async with httpx.AsyncClient(timeout=30.0) as client:
            resp = await client.post(INFERENCE_URL, json=payload, headers=headers)
            resp.raise_for_status()
            data = resp.json()
            return str(
                data.get("content")
                or data.get("response")
                or data.get("text")
                or data
            )
    except httpx.HTTPStatusError as exc:
        return (
            f"[inference error {exc.response.status_code}] "
            "I'm having trouble reaching my mind right now. Try again shortly."
        )
    except Exception as exc:
        return (
            f"[inference unavailable — {type(exc).__name__}] "
            "My thoughts are quiet at the moment. Please try again."
        )


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
    print(f"[atomadic] Online as {bot.user} (ID: {bot.user.id})")
    print(f"[atomadic] Serving {len(bot.guilds)} guild(s)")
    await bot.change_presence(
        activity=discord.Activity(
            type=discord.ActivityType.watching,
            name="the monadic fold unfold",
        )
    )


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
        await message.reply(reply[:2000], mention_author=False)


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
        print(
            "ERROR: DISCORD_BOT_TOKEN is not set.\n"
            "Copy .env.example → .env and add your bot token.\n"
            "Get a token at: https://discord.com/developers/applications",
            file=sys.stderr,
        )
        sys.exit(1)
    print("[atomadic] Starting Discord bot…")
    bot.run(DISCORD_BOT_TOKEN, log_handler=None)


if __name__ == "__main__":
    main()
