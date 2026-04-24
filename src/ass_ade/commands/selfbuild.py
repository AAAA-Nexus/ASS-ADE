"""Tier a4 — CLI: ``ass-ade selfbuild`` — rebuild ASS-ADE and its siblings.

Runs ``rebuild_project`` over every ``C:\\!ass-ade*`` folder (or a custom
glob) so the canonical monadic decomposition is regenerated into a fresh
tier-partitioned output tree. The rebuild does NOT mutate the source
repos; it emits a new folder under ``--out``.
"""

from __future__ import annotations

import os
import shutil
from pathlib import Path
from typing import Annotated

import typer
from rich.console import Console
from rich.table import Table

from ass_ade.a1_at_functions.assimilation_target_map import (
    build_assimilation_target_map,
    dumps_target_map,
)
from ass_ade.engine.rebuild.orchestrator import rebuild_project, render_rebuild_summary

selfbuild_app = typer.Typer(
    help="Run the monadic rebuild over ASS-ADE itself and its sibling !ass-ade* repos."
)
_console = Console()


def _discover_siblings(parent: Path, pattern: str, exclude: list[Path] | None = None) -> list[Path]:
    """Find matching sibling directories containing Python source."""
    exclude_resolved = {p.resolve() for p in (exclude or [])}
    matches: list[Path] = []
    for entry in sorted(parent.glob(pattern)):
        if not entry.is_dir():
            continue
        if entry.resolve() in exclude_resolved:
            continue
        # Skip VCS, caches, venvs.
        if entry.name.startswith("."):
            continue
        # Prefer src/ layout when present, else the repo root.
        src = entry / "src"
        matches.append(src if src.is_dir() else entry)
    return matches


@selfbuild_app.command("run")
def run(
    parent: Path = typer.Option(
        Path("C:/"), "--parent", "-p", help="Parent folder containing !ass-ade* siblings."
    ),
    pattern: str = typer.Option(
        "!ass-ade*", "--pattern", help="Glob pattern for sibling repos."
    ),
    out: Path = typer.Option(
        Path("./.ass-ade/selfbuild"), "--out", "-o", help="Output directory."
    ),
    synthesize: bool = typer.Option(
        False, "--synthesize", help="Fill gaps via AAAA-Nexus (requires API key)."
    ),
    max_synthesize: int = typer.Option(
        20, "--max-synthesize", help="Cap on components to synthesize."
    ),
    tag: str = typer.Option(
        None, "--tag", help="Explicit output subfolder name (default: timestamped)."
    ),
    final_dir: Path = typer.Option(
        None,
        "--final-dir",
        help="Absolute destination. Rebuild runs in a scratch parent and the "
             "tagged folder is renamed to this path on success.",
    ),
    dry_run: bool = typer.Option(
        False, "--dry-run", help="List discovered sources only; do not rebuild."
    ),
) -> None:
    """Discover !ass-ade* siblings and rebuild them into one monadic tree."""
    parent = parent.resolve()
    if not parent.is_dir():
        _console.print(f"[red]parent not a directory:[/red] {parent}")
        raise typer.Exit(code=1)
    exclude = [final_dir] if final_dir is not None else None
    sources = _discover_siblings(parent, pattern, exclude=exclude)
    if not sources:
        _console.print(f"[yellow]no matches for[/yellow] {parent}/{pattern}")
        raise typer.Exit(code=1)

    table = Table(title="Sibling sources")
    table.add_column("path")
    for s in sources:
        table.add_row(str(s))
    _console.print(table)

    if dry_run:
        _console.print("[dim]dry-run: no rebuild performed[/dim]")
        return

    # If --final-dir is set, rebuild into a scratch parent then rename.
    if final_dir is not None:
        final_dir = final_dir.resolve()
        effective_tag = tag or "current"
        scratch = final_dir.parent / f".ass-ade-selfbuild-scratch-{os.getpid()}"
        if scratch.exists():
            shutil.rmtree(scratch, ignore_errors=True)
        scratch.mkdir(parents=True, exist_ok=True)
        rebuild_out = scratch
    else:
        out.mkdir(parents=True, exist_ok=True)
        rebuild_out = out
        effective_tag = tag

    _console.print(f"[bold]rebuilding[/bold] {len(sources)} source(s) -> {rebuild_out}")
    result = rebuild_project(
        source_path=sources,
        output_dir=rebuild_out,
        synthesize_gaps=synthesize,
        nexus_api_key=os.environ.get("AAAA_NEXUS_API_KEY") if synthesize else None,
        nexus_agent_id=os.environ.get("AAAA_NEXUS_AGENT_ID") if synthesize else None,
        max_synthesize=max_synthesize,
        rebuild_tag=effective_tag,
    )
    _console.print(render_rebuild_summary(result))

    if final_dir is not None:
        built_root = Path(result["phases"]["materialize"]["target_root"])
        if final_dir.exists():
            shutil.rmtree(final_dir)
        shutil.move(str(built_root), str(final_dir))
        shutil.rmtree(scratch, ignore_errors=True)
        _console.print(f"[green]final:[/green] {final_dir}")


@selfbuild_app.command("target-map")
def target_map(
    primary: Annotated[
        Path,
        typer.Option(
            "--primary",
            "-m",
            exists=True,
            file_okay=False,
            dir_okay=True,
            resolve_path=True,
            help="Primary MAP terrain. Defaults to the current directory.",
        ),
    ] = Path("."),
    sibling: Annotated[
        list[Path] | None,
        typer.Option(
            "--sibling",
            "-s",
            exists=True,
            file_okay=False,
            dir_okay=True,
            resolve_path=True,
            help="Sibling root to map. May be repeated.",
        ),
    ] = None,
    parent: Annotated[
        Path | None,
        typer.Option(
            "--parent",
            "-p",
            file_okay=False,
            dir_okay=True,
            resolve_path=True,
            help="Parent folder for glob discovery when --sibling is omitted.",
        ),
    ] = None,
    pattern: Annotated[
        str,
        typer.Option("--pattern", help="Glob used with --parent."),
    ] = "!ass-ade*",
    focus: Annotated[
        list[str] | None,
        typer.Option(
            "--focus",
            "-f",
            help="Only include symbols whose module or qualname contains this text.",
        ),
    ] = None,
    out: Annotated[
        Path | None,
        typer.Option(
            "--out",
            "-o",
            file_okay=True,
            dir_okay=False,
            help="Write target map JSON to this path.",
        ),
    ] = None,
) -> None:
    """Map sibling functions/features into assimilate, rebuild, enhance, or skip targets."""
    primary = primary.resolve()
    siblings = list(sibling or [])
    if not siblings and parent is not None:
        siblings = _discover_siblings(parent.resolve(), pattern, exclude=[primary])
    siblings = [path.resolve() for path in siblings if path.resolve() != primary]
    if not siblings:
        _console.print("[red]no sibling roots supplied or discovered[/red]")
        raise typer.Exit(code=2)

    result = build_assimilation_target_map(
        primary_root=primary,
        sibling_roots=siblings,
        focus=focus or [],
    )
    payload = dumps_target_map(result)
    if out is not None:
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(payload, encoding="utf-8")
        _console.print(f"[green]target map written:[/green] {out}")
    else:
        typer.echo(payload)


def register_selfbuild_app(parent: typer.Typer) -> None:
    """Mount ``selfbuild`` under a parent Typer app."""
    parent.add_typer(selfbuild_app, name="selfbuild")
