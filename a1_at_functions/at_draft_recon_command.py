# Extracted from C:/!ass-ade/src/ass_ade/cli.py:4217
# Component id: at.source.ass_ade.recon_command
from __future__ import annotations

__version__ = "0.1.0"

def recon_command(
    path: Path = typer.Argument(Path("."), help="Repo root to analyse."),
    out: Path | None = typer.Option(None, "--out", "-o", help="Write RECON_REPORT.md to this file."),
    json_out: bool = typer.Option(False, "--json", help="Print JSON instead of Markdown."),
) -> None:
    """Run parallel codebase reconnaissance — 5 agents, no LLM, < 5 s.

    Agents: Scout (files/structure), Dependency (imports/cycles),
    Tier (qk/at/mo/og/sy), Test (coverage), Doc (README/docstrings).
    """
    import json as _json
    from ass_ade.recon import run_parallel_recon

    target = path.resolve()
    if not target.exists():
        console.print(f"[red]Path does not exist:[/red] {target}")
        raise typer.Exit(code=1)

    console.print(f"[bold]Running recon on[/bold] {target} …")
    report = run_parallel_recon(target)

    if json_out:
        console.print_json(_json.dumps(report.to_dict(), indent=2))
    else:
        console.print(report.to_markdown())

    if out:
        out.write_text(report.to_markdown(), encoding="utf-8")
        console.print(f"[green]Report written →[/green] {out}")

    console.print(f"[dim]Completed in {report.duration_ms:.0f} ms[/dim]")
