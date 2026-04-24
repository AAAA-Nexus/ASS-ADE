"""Scout command: repo intel plus LLM synthesis."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Annotated

import typer
from rich.console import Console
from rich.table import Table

from ass_ade.local.scout import scout_repo

console = Console()
_DEFAULT_REPO = Path(".")


def scout_command(
    repo: Annotated[
        Path,
        typer.Argument(
            exists=True,
            file_okay=False,
            dir_okay=True,
            resolve_path=True,
            help="Repository to scout.",
        ),
    ] = _DEFAULT_REPO,
    benefit_root: Annotated[
        Path | None,
        typer.Option(
            "--benefit-root",
            "-b",
            exists=True,
            file_okay=False,
            dir_okay=True,
            resolve_path=True,
            help="Primary repo to compare against for ASS-ADE benefit mapping.",
        ),
    ] = _DEFAULT_REPO,
    llm: Annotated[
        bool,
        typer.Option("--llm/--no-llm", help="Use the configured LLM provider for scout synthesis."),
    ] = True,
    nexus_guards: Annotated[
        bool,
        typer.Option(
            "--nexus-guards/--no-nexus-guards",
            help="Run AAAA-Nexus hallucination, trust, certification, and drift guards on LLM scout output.",
        ),
    ] = True,
    model: Annotated[
        str | None,
        typer.Option("--model", help="Override model id for this scout run."),
    ] = None,
    config: Annotated[
        Path | None,
        typer.Option("--config", file_okay=True, dir_okay=False, help="ASS-ADE config path."),
    ] = None,
    json_out: Annotated[
        Path | None,
        typer.Option("--json-out", file_okay=True, dir_okay=False, help="Write full scout JSON."),
    ] = None,
    print_json: Annotated[
        bool,
        typer.Option("--json", help="Print full scout JSON to stdout."),
    ] = False,
) -> None:
    """Scout a repo and report what it contains, risks, and useful ASS-ADE opportunities."""
    benefit = benefit_root.resolve() if benefit_root is not None else None
    if benefit == repo.resolve():
        benefit = None
    report = scout_repo(
        repo,
        benefit_root=benefit,
        use_llm=llm,
        nexus_guards=nexus_guards,
        config_path=config,
        model=model,
    )
    payload = json.dumps(report, indent=2, default=str) + "\n"
    if json_out is not None:
        json_out.parent.mkdir(parents=True, exist_ok=True)
        json_out.write_text(payload, encoding="utf-8")
        console.print(f"[green]scout report written:[/green] {json_out}")
    if print_json:
        typer.echo(payload)
        return
    _print_summary(report)


def _print_summary(report: dict[str, object]) -> None:
    summary = report.get("summary") if isinstance(report.get("summary"), dict) else {}
    symbols = report.get("symbol_summary") if isinstance(report.get("symbol_summary"), dict) else {}
    console.print(f"[bold]Scout:[/bold] {report.get('repo')}")
    table = Table(title="Repo Intel")
    table.add_column("Signal")
    table.add_column("Value")
    table.add_row("Files", str(summary.get("total_files", 0)))
    table.add_row("Directories", str(summary.get("total_dirs", 0)))
    table.add_row("Python files", str(symbols.get("python_files", 0)))
    table.add_row("Symbols", str(symbols.get("symbols", 0)))
    table.add_row("Tested symbols", str(symbols.get("tested_symbols", 0)))
    llm = report.get("llm") if isinstance(report.get("llm"), dict) else {}
    table.add_row("LLM", str(llm.get("status", "unknown")))
    console.print(table)

    target_map = report.get("target_map") if isinstance(report.get("target_map"), dict) else None
    if target_map:
        console.print(f"[bold]Benefit action counts:[/bold] {target_map.get('action_counts')}")

    recs = report.get("static_recommendations")
    if isinstance(recs, list) and recs:
        console.print("[bold]Static recommendations[/bold]")
        for rec in recs[:8]:
            if isinstance(rec, dict):
                console.print(
                    f"- priority={rec.get('priority')} type={rec.get('type')}: {rec.get('title')}"
                )

    if isinstance(llm, dict) and llm.get("status") == "ok":
        analysis = llm.get("analysis")
        grounding = llm.get("grounding_guard")
        nexus = llm.get("nexus_guards")
        if isinstance(grounding, dict):
            console.print(f"[bold]Grounding guard:[/bold] {grounding.get('status')}")
        if isinstance(nexus, dict):
            console.print(
                f"[bold]Nexus guards:[/bold] {nexus.get('status')} passed={nexus.get('passed')}"
            )
        console.print("[bold]LLM scout synthesis[/bold]")
        if isinstance(analysis, dict):
            for key in ("summary", "benefit_thesis"):
                if analysis.get(key):
                    console.print(f"{key}: {analysis[key]}")
            opportunities = analysis.get("opportunities")
            if isinstance(opportunities, list):
                for item in opportunities[:6]:
                    console.print(f"- {item}")
        else:
            console.print(str(analysis))
    elif isinstance(llm, dict) and llm.get("status") == "unavailable":
        console.print(f"[yellow]LLM unavailable:[/yellow] {llm.get('error')}")
