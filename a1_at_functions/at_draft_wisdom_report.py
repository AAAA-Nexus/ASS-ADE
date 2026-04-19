# Extracted from C:/!ass-ade/src/ass_ade/cli.py:3885
# Component id: at.source.ass_ade.wisdom_report
from __future__ import annotations

__version__ = "0.1.0"

def wisdom_report(
    last: int = typer.Option(10, help="Number of recent audit cycles to show."),
) -> None:
    """Show WisdomEngine audit history, conviction trend, and distilled principles."""
    from ass_ade.agent.wisdom import WisdomEngine

    engine = WisdomEngine({})
    rep = engine.report()
    t = Table(title="WisdomEngine Report")
    t.add_column("Metric")
    t.add_column("Value")
    t.add_row("Audits completed", str(rep.get("audits", 0)))
    t.add_row("Current conviction", f"{rep.get('conviction', 0.0):.2%}")
    t.add_row("Conviction required", f"{rep.get('conviction_required', 0.85):.2%}")
    t.add_row("Confident", "YES" if rep.get("conviction", 0) >= rep.get("conviction_required", 0.85) else "NO")
    console.print(t)

    principles = rep.get("principles", [])
    if principles:
        console.print("\n[bold]Distilled Principles:[/bold]")
        for i, p in enumerate(principles[:last], 1):
            console.print(f"  {i}. {p}")
    else:
        console.print("[dim]No principles distilled yet. Run agent sessions to populate.[/dim]")
