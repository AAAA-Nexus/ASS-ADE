"""Tier a4 — `ass-ade assimilate` command: copy cherry-picked symbols into the target project's tier dirs."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Annotated, Optional

import typer
from rich.console import Console
from rich.table import Table

console = Console()
_DEFAULT_MANIFEST = Path(".ass-ade/cherry_pick.json")
_VALID_TIERS = ("a1_at_functions", "a2_mo_composites", "a3_og_features", "a4_sy_orchestration")


def assimilate_command(
    manifest: Annotated[
        Path,
        typer.Argument(
            exists=True,
            file_okay=True,
            dir_okay=False,
            resolve_path=True,
            help="Cherry-pick manifest JSON (from ass-ade cherry-pick). Default: .ass-ade/cherry_pick.json",
        ),
    ] = _DEFAULT_MANIFEST,
    target: Annotated[
        Optional[Path],
        typer.Option(
            "--target",
            "-t",
            file_okay=False,
            dir_okay=True,
            resolve_path=True,
            help="Override the target project root stored in the manifest.",
        ),
    ] = None,
    dry_run: Annotated[
        bool,
        typer.Option("--dry-run", help="Plan the assimilation but write nothing to disk."),
    ] = False,
    tier_override: Annotated[
        Optional[str],
        typer.Option(
            "--tier",
            help=f"Force all symbols into this tier. Choices: {', '.join(_VALID_TIERS)}",
        ),
    ] = None,
    report_json: Annotated[
        Optional[Path],
        typer.Option(
            "--report-json",
            file_okay=True,
            dir_okay=False,
            help="Write the assimilation report JSON to this path.",
        ),
    ] = None,
    print_json: Annotated[
        bool,
        typer.Option("--json", help="Print the assimilation report JSON to stdout."),
    ] = False,
) -> None:
    """Assimilate cherry-picked symbols into the target project's monadic tier directories.

    Reads a cherry_pick.json manifest (produced by `ass-ade cherry-pick`) and copies each
    selected symbol into the correct tier directory of the target project:

    \\b
      function → a1_at_functions/<slug>_helpers.py
      class    → a2_mo_composites/<slug>_core.py
      method   → a2_mo_composites/<slug>_core.py

    Each output file gets a tier docstring header and a commented import block from the
    original module so you can resolve dependencies manually or via `ass-ade lint`.

    \\b
    Examples:
        ass-ade assimilate
        ass-ade assimilate scout_cherry.json --target ./my-project --dry-run
        ass-ade assimilate cherry_pick.json --tier a1_at_functions
        ass-ade assimilate cherry_pick.json --report-json assimilation_report.json
    """
    from ass_ade.a3_og_features.assimilate_feature import assimilation_report, run_assimilate

    if tier_override and tier_override not in _VALID_TIERS:
        console.print(f"[red]Invalid --tier {tier_override!r}. Choose from: {', '.join(_VALID_TIERS)}[/red]")
        raise typer.Exit(1)

    try:
        results = run_assimilate(
            manifest_path=manifest,
            target_root=target,
            dry_run=dry_run,
            tier_override=tier_override,
            console_print=True,
        )
    except (ValueError, OSError, KeyError) as exc:
        console.print(f"[red]assimilate error:[/red] {exc}")
        raise typer.Exit(1) from exc

    report = assimilation_report(results)
    _print_rich_summary(report, dry_run=dry_run)

    if report_json is not None:
        payload = json.dumps(report, indent=2) + "\n"
        report_json.parent.mkdir(parents=True, exist_ok=True)
        report_json.write_text(payload, encoding="utf-8")
        console.print(f"[green]Report written:[/green] {report_json}")

    if print_json:
        typer.echo(json.dumps(report, indent=2))

    # Non-zero exit if any errors
    if report.get("by_status", {}).get("error", 0) > 0:
        raise typer.Exit(1)


def _print_rich_summary(report: dict, *, dry_run: bool) -> None:
    prefix = "[DRY RUN] " if dry_run else ""
    table = Table(title=f"{prefix}Assimilation Summary", show_lines=False)
    table.add_column("Status")
    table.add_column("Count", justify="right")
    for status, count in sorted((report.get("by_status") or {}).items()):
        table.add_row(status, str(count))
    console.print(table)

    items_by_status: dict = report.get("items", {})
    written = items_by_status.get("written", [])
    if written:
        verb = "Would write" if dry_run else "Written"
        w_table = Table(title=f"{verb}", show_lines=False)
        w_table.add_column("Target file")
        w_table.add_column("Tier")
        w_table.add_column("LOC", justify="right")
        for item in written[:30]:
            w_table.add_row(item["target_file"], item["tier"], str(item["lines"]))
        if len(written) > 30:
            console.print(f"  … and {len(written) - 30} more")
        console.print(w_table)
