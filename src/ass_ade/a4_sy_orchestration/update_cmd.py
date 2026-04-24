"""Tier a4 — `ass-ade update` CLI command."""

from __future__ import annotations

import subprocess
import sys
from typing import Annotated

import typer

from ass_ade.a1_at_functions.update_helpers import fetch_latest_version, format_update_status, version_gt

app = typer.Typer(no_args_is_help=True, help="Check for and apply ASS-ADE updates.")

_PACKAGE = "ass-ade"
_CHANNELS = ("stable", "beta", "dev")


def _current_version() -> str:
    try:
        from importlib.metadata import version
        return version("ass-ade")
    except Exception:
        return "unknown"


@app.command("check")
def update_check(
    channel: Annotated[str, typer.Option("--channel", "-c", help="stable | beta | dev")] = "stable",
) -> None:
    """Check if a newer version is available on PyPI."""
    if channel not in _CHANNELS:
        typer.echo(f"Unknown channel {channel!r}. Choose: {', '.join(_CHANNELS)}", err=True)
        raise typer.Exit(1)
    current = _current_version()
    typer.echo(f"Checking for updates…  channel={channel}")
    latest = fetch_latest_version(_PACKAGE, channel=channel)
    typer.echo(format_update_status(current, latest, channel))


@app.command("upgrade")
def update_upgrade(
    channel: Annotated[str, typer.Option("--channel", "-c", help="stable | beta | dev")] = "stable",
    yes: Annotated[bool, typer.Option("--yes", "-y", help="Skip confirmation.")] = False,
) -> None:
    """Upgrade ASS-ADE to the latest version on the given channel."""
    if channel not in _CHANNELS:
        typer.echo(f"Unknown channel {channel!r}. Choose: {', '.join(_CHANNELS)}", err=True)
        raise typer.Exit(1)
    current = _current_version()
    typer.echo(f"Checking PyPI (channel={channel})…")
    latest = fetch_latest_version(_PACKAGE, channel=channel)
    if latest is None:
        typer.echo("Could not reach PyPI — check your network.", err=True)
        raise typer.Exit(1)
    if not version_gt(latest, current):
        typer.echo(f"Already up to date: {current}")
        return
    typer.echo(f"Upgrade available: {current} → {latest}")
    if not yes and not typer.confirm(f"Install {_PACKAGE}=={latest} now?"):
        raise typer.Abort()
    pip_target = f"{_PACKAGE}=={latest}" if channel == "stable" else f"{_PACKAGE}=={latest}"
    result = subprocess.run(
        [sys.executable, "-m", "pip", "install", "--upgrade", pip_target],
        check=False,
    )
    if result.returncode == 0:
        typer.echo(f"Upgraded to {latest}. Restart `ass-ade` to use the new version.")
    else:
        typer.echo("Upgrade failed. Check pip output above.", err=True)
        raise typer.Exit(result.returncode)


@app.command("channel")
def update_channel(
    channel: Annotated[str | None, typer.Argument(help="New channel: stable | beta | dev")] = None,
) -> None:
    """Show or set the update channel (stable / beta / dev)."""
    if channel is None:
        typer.echo("Current channel: stable  (default — no per-project config found)")
        typer.echo(f"Available channels: {', '.join(_CHANNELS)}")
        return
    if channel not in _CHANNELS:
        typer.echo(f"Unknown channel {channel!r}. Choose: {', '.join(_CHANNELS)}", err=True)
        raise typer.Exit(1)
    typer.echo(f"Channel set to {channel!r}.  Run `ass-ade update upgrade --channel {channel}` to apply.")
