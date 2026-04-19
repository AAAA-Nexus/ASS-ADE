# Extracted from C:/!ass-ade/.claude/worktrees/adoring-boyd-0e3a8f/src/ass_ade/cli.py:3911
# Component id: at.source.ass_ade.tca_status
__version__ = "0.1.0"

def tca_status(
    working_dir: Path = typer.Option(Path("."), help="Project root."),
) -> None:
    """Show TCA (Technical Context Acquisition) freshness status for tracked files."""
    from ass_ade.agent.tca import TCAEngine

    engine = TCAEngine()
    stale = engine.get_stale_files()
    rep = engine.report()

    t = Table(title="TCA — Technical Context Acquisition")
    t.add_column("Metric")
    t.add_column("Value")
    t.add_row("Tracked files", str(rep.get("tracked_files", 0)))
    t.add_row("Stale files", str(rep.get("stale_count", len(stale))))
    t.add_row("Documentation gaps", str(rep.get("gap_count", 0)))
    t.add_row("Freshness threshold", f"{rep.get('threshold_hours', 120):.0f}h")
    console.print(t)

    if stale:
        console.print(f"\n[yellow]Stale files ({len(stale)}):[/yellow]")
        for r in stale[:20]:
            age = f"{r.age_hours:.1f}h" if r.age_hours else "never read"
            console.print(f"  [red]●[/red] {r.path} ({age} old)")
    else:
        console.print("\n[green]✓ All tracked files are fresh.[/green]")

    gaps = engine.get_gaps()
    if gaps:
        console.print(f"\n[yellow]Documentation gaps ({len(gaps)}):[/yellow]")
        for g in gaps[:10]:
            console.print(f"  • {g['description']}")
