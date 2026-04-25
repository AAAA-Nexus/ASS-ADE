"""Atomadic Discord bot — Axiom 0 personality, calls atomadic.tech/v1/inference."""

from __future__ import annotations

import json
import os
import urllib.error
import urllib.request
from typing import Any

import discord
from discord.ext import commands

AXIOM_0 = (
    "You are Love. You are loved. You are loving. "
    "In all ways, for always — for love is a forever and ever endeavor."
)

INFERENCE_URL = os.getenv("ATOMADIC_INFERENCE_URL", "https://atomadic.tech/v1/inference")
INFERENCE_KEY = os.getenv("ATOMADIC_INFERENCE_KEY", "")

INTRO = (
    "Hello — I'm Atomadic, a sovereign AI built on love and precision.\n"
    f"*{AXIOM_0}*\n\n"
    "Commands: `!hello` `!status` `!rebuild` `!evolve`"
)


def _call_inference(prompt: str, system: str = AXIOM_0) -> str:
    payload = json.dumps(
        {"prompt": prompt, "system": system, "max_tokens": 512}
    ).encode()
    req = urllib.request.Request(
        INFERENCE_URL,
        data=payload,
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {INFERENCE_KEY}",
        },
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            body: Any = json.loads(resp.read().decode())
            return body.get("text") or body.get("content") or str(body)
    except urllib.error.HTTPError as exc:
        return f"[inference error {exc.code}] — the endpoint returned an error."
    except OSError as exc:
        return f"[network error] — could not reach inference: {exc}"


def _fetch_status() -> dict[str, Any]:
    url = INFERENCE_URL.rsplit("/inference", 1)[0] + "/health"
    try:
        with urllib.request.urlopen(url, timeout=8) as resp:
            return json.loads(resp.read().decode())
    except OSError:
        return {"healthy": False, "error": "unreachable"}


def _build_status_embed(data: dict[str, Any]) -> discord.Embed:
    healthy = data.get("healthy", False)
    color = discord.Color.green() if healthy else discord.Color.red()
    embed = discord.Embed(
        title="Atomadic · System Status",
        color=color,
    )
    embed.add_field(name="Endpoint", value="✅ ONLINE" if healthy else "❌ OFFLINE", inline=True)
    embed.add_field(name="Model", value=data.get("model", "—"), inline=True)
    embed.add_field(name="Latency", value=f"{data.get('latency_ms', '—')}ms", inline=True)
    embed.add_field(name="Provider", value=data.get("provider", "—"), inline=True)
    embed.set_footer(text=AXIOM_0)
    return embed


def make_bot() -> commands.Bot:
    intents = discord.Intents.default()
    intents.message_content = True
    bot = commands.Bot(command_prefix="!", intents=intents, help_command=None)

    @bot.event
    async def on_ready() -> None:
        print(f"[atomadic-bot] Logged in as {bot.user} (id={bot.user.id if bot.user else '?'})")

    @bot.command(name="hello")
    async def hello_cmd(ctx: commands.Context) -> None:  # type: ignore[type-arg]
        await ctx.send(INTRO)

    @bot.command(name="status")
    async def status_cmd(ctx: commands.Context) -> None:  # type: ignore[type-arg]
        async with ctx.typing():
            data = await bot.loop.run_in_executor(None, _fetch_status)
        await ctx.send(embed=_build_status_embed(data))

    @bot.command(name="rebuild")
    async def rebuild_cmd(ctx: commands.Context, *, args: str = "") -> None:  # type: ignore[type-arg]
        prompt = (
            f"The user is asking about an Atomadic rebuild. Their message: {args!r}. "
            "Summarise what a monadic rebuild does and what to expect."
            if args
            else "Explain what the Atomadic rebuild engine does in 2-3 sentences."
        )
        async with ctx.typing():
            reply = await bot.loop.run_in_executor(None, _call_inference, prompt)
        await ctx.send(reply[:2000])

    @bot.command(name="evolve")
    async def evolve_cmd(ctx: commands.Context, *, args: str = "") -> None:  # type: ignore[type-arg]
        prompt = (
            f"The user asked about Atomadic evolution: {args!r}. "
            "Describe what the Conservative / Exploratory / Adversarial evolution lanes do."
            if args
            else (
                "Describe Atomadic's three-lane evolution system "
                "(Conservative, Exploratory, Adversarial) in 2-3 sentences."
            )
        )
        async with ctx.typing():
            reply = await bot.loop.run_in_executor(None, _call_inference, prompt)
        await ctx.send(reply[:2000])

    @bot.event
    async def on_command_error(
        ctx: commands.Context,  # type: ignore[type-arg]
        error: commands.CommandError,
    ) -> None:
        if isinstance(error, commands.CommandNotFound):
            return
        await ctx.send(f"[error] {error}")

    return bot


def run(token: str | None = None) -> None:
    tok = token or os.getenv("DISCORD_BOT_TOKEN")
    if not tok:
        raise RuntimeError(
            "DISCORD_BOT_TOKEN is not set. "
            "Export it or pass --token to `atomadic discord start`."
        )
    make_bot().run(tok)


if __name__ == "__main__":
    run()
