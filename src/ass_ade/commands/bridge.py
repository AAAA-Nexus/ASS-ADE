"""Tier a4 — `ass-ade bridge` subcommand group for multi-language bridge operations."""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Annotated, Optional

import typer

app = typer.Typer(
    no_args_is_help=True,
    help="Multi-language bridge: generate TypeScript/Rust/Kotlin/Swift scaffolding that calls ASS-ADE.",
)


@app.command("init")
def bridge_init(
    target: Annotated[
        Path,
        typer.Argument(
            file_okay=False,
            dir_okay=True,
            resolve_path=True,
            help="Target repo root where the bridge will be generated (default: current directory).",
        ),
    ] = Path("."),
    lang: Annotated[
        str,
        typer.Option(
            "--lang",
            "-l",
            help="Bridge language to emit (currently: typescript).",
        ),
    ] = "typescript",
    python_cmd: Annotated[
        Optional[str],
        typer.Option(
            "--python-cmd",
            help='Python command to run ass-ade, space-separated (default: "<sys.executable> -m ass_ade").',
        ),
    ] = None,
    project_name: Annotated[
        Optional[str],
        typer.Option("--name", help="Project name for generated files (default: target directory name)."),
    ] = None,
    bridge_ready: Annotated[
        bool,
        typer.Option(
            "--ready/--no-ready",
            help="Mark bridge_ready=true in the manifest (default: true when --python-cmd is set).",
        ),
    ] = True,
) -> None:
    """Generate multi-language bridge scaffolding in a target repository.

    The bridge lets TypeScript (and other) code call ASS-ADE Python commands
    via subprocess spawn.  After running this command:

    \\b
      1. Edit ``.ass-ade/bridges/bridge_manifest.json`` if needed.
      2. ``cd <target>/bridges/typescript && npm install && npm run smoke``

    Examples:
        ass-ade bridge init .
        ass-ade bridge init C:/projects/my-ts-app --lang typescript
        ass-ade bridge init C:/!aaaa-nexus/ass-claw-repos/openclaw
    """
    from ass_ade.local.multilang_bridge import generate_typescript_bridge

    if lang != "typescript":
        typer.echo(f"[warn] Only 'typescript' is currently implemented. Got: {lang!r}", err=True)
        raise typer.Exit(1)

    cmd: list[str] | None = None
    if python_cmd:
        cmd = python_cmd.split()
    else:
        cmd = [sys.executable, "-m", "ass_ade"]

    result = generate_typescript_bridge(
        target,
        python_bridge_command=cmd,
        project_name=project_name or "",
        bridge_ready=bridge_ready,
    )

    typer.echo(f"OK — TypeScript bridge written to: {result['target_dir']}")
    typer.echo(f"  manifest: {result['manifest_path']}")
    typer.echo(f"  files written: {result['files_written']}")
    typer.echo(f"  bridge_ready: {result['bridge_ready']}")
    typer.echo(f"  python command: {' '.join(result['python_bridge_command'])}")
    typer.echo("")
    typer.echo("Next steps:")
    typer.echo(f"  cd {result['target_dir']}/bridges/typescript")
    typer.echo("  npm install")
    typer.echo("  node smoke.mjs   # verify bridge reads manifest correctly")


@app.command("status")
def bridge_status(
    target: Annotated[
        Path,
        typer.Argument(
            file_okay=False,
            dir_okay=True,
            resolve_path=True,
            help="Repo root to check (default: current directory).",
        ),
    ] = Path("."),
    json_out: Annotated[
        bool,
        typer.Option("--json", help="Print status as JSON."),
    ] = False,
) -> None:
    """Show bridge manifest status for a repository."""
    manifest_path = target / ".ass-ade" / "bridges" / "bridge_manifest.json"
    if not manifest_path.exists():
        if json_out:
            typer.echo(json.dumps({"bridge_ready": False, "manifest": None}))
        else:
            typer.echo(f"No bridge manifest found at: {manifest_path}")
            typer.echo("Run `ass-ade bridge init` to generate one.")
        raise typer.Exit(1)

    payload = json.loads(manifest_path.read_text(encoding="utf-8"))
    if json_out:
        typer.echo(json.dumps(payload, indent=2))
    else:
        ready = payload.get("bridge_ready", False)
        langs = ", ".join(payload.get("bridge_languages", []))
        cmd = " ".join(payload.get("python_bridge_command", []))
        status_icon = "OK" if ready else "NOT READY"
        typer.echo(f"Bridge status: {status_icon}")
        typer.echo(f"  schema:   {payload.get('schema', '?')}")
        typer.echo(f"  languages: {langs or '(none)'}")
        typer.echo(f"  command:   {cmd or '(not configured)'}")
        typer.echo(f"  manifest:  {manifest_path}")
