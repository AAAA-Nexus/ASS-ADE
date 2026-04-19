# Extracted from C:/!ass-ade/src/ass_ade/cli.py:3868
# Component id: at.source.ass_ade.sam_status
from __future__ import annotations

__version__ = "0.1.0"

def sam_status() -> None:
    """Show SAM TRS scoring status and G23 gate history for the current session."""
    from ass_ade.agent.sam import SAM

    sam = SAM({})
    rep = sam.report()
    t = Table(title="SAM — Sovereign Assessment Matrix")
    t.add_column("Metric")
    t.add_column("Value")
    t.add_row("Total checks", str(rep.get("checks", 0)))
    t.add_row("G23 threshold", str(rep.get("g23_threshold", 7)))
    t.add_row("Engine", rep.get("engine", "sam"))
    console.print(t)
    console.print("[dim]Run an agent session to populate TRS history.[/dim]")
