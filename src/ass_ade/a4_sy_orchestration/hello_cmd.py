"""Tier a4 — CLI commands for the hello.atomadic.tech Cloudflare Worker."""

from __future__ import annotations

import subprocess
from pathlib import Path
from typing import Annotated

import typer

hello_app = typer.Typer(
    name="hello",
    help="hello.atomadic.tech Cloudflare Worker — deploy and manage the landing page.",
    no_args_is_help=True,
)

_CHECKOUT_ROOT = Path(__file__).resolve().parents[3]


@hello_app.command("deploy")
def deploy(
    env: Annotated[
        str,
        typer.Option("--env", "-e", help="Wrangler environment (default: production)."),
    ] = "production",
    dry_run: Annotated[
        bool,
        typer.Option("--dry-run", help="Print the wrangler command without executing it."),
    ] = False,
) -> None:
    """Deploy hello.atomadic.tech via Wrangler.

    Requires Node.js and wrangler installed (npx wrangler is used automatically).
    Set CLOUDFLARE_API_TOKEN in your environment or .env before deploying.
    """
    wrangler_toml = _CHECKOUT_ROOT / "wrangler.toml"
    worker_script = _CHECKOUT_ROOT / "scripts" / "hello_worker.js"

    for path, label in [(wrangler_toml, "wrangler.toml"), (worker_script, "hello_worker.js")]:
        if not path.exists():
            typer.secho(f"{label} not found: {path}", fg=typer.colors.RED, err=True)
            raise typer.Exit(1)

    cmd = [
        "npx", "wrangler", "deploy",
        "--config", str(wrangler_toml),
        "--env", env,
    ]

    typer.secho(f"Deploy command: {' '.join(cmd)}", fg=typer.colors.CYAN)
    typer.secho(f"Worker:         {worker_script}", fg=typer.colors.CYAN)
    typer.secho(f"Environment:    {env}", fg=typer.colors.CYAN)

    if dry_run:
        typer.secho("\n[dry-run] Command not executed.", fg=typer.colors.YELLOW)
        return

    result = subprocess.run(cmd, cwd=str(_CHECKOUT_ROOT))
    raise typer.Exit(result.returncode)
