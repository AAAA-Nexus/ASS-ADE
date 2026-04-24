"""Tier a1 — assimilated function 'run'

Assimilated from: selfbuild.py:46-135
"""

from __future__ import annotations


# --- assimilated symbol ---
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
    try:
        from ass_ade.engine.registry import default_registry

        registry_snapshot = default_registry().snapshot()
    except Exception:
        registry_snapshot = None
    result = rebuild_project(
        source_path=sources,
        output_dir=rebuild_out,
        registry=registry_snapshot,
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

