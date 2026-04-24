"""Wire command: scan tier imports and optionally patch upward violations.

Dry-run by default — only writes to disk when ``--apply`` is passed.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Annotated

import typer
from rich.console import Console
from rich.table import Table

from ass_ade.a2_mo_composites.context_loader_wiring_specialist_core import (
    ContextLoaderWiringSpecialist,
)


console = Console()


def wire_command(
    source: Annotated[
        Path,
        typer.Argument(
            exists=True,
            file_okay=False,
            dir_okay=True,
            resolve_path=True,
            help="Source tree to scan (defaults to ./src/<pkg> if found, else cwd).",
        ),
    ] = Path("."),
    apply: Annotated[
        bool,
        typer.Option(
            "--apply",
            help="Actually patch files on disk. Without this flag, wire runs in dry-run mode.",
        ),
    ] = False,
    package_name: Annotated[
        str | None,
        typer.Option(
            "--package",
            help="Python package name for auto-fix import generation. Inferred from pyproject.toml if omitted.",
        ),
    ] = None,
    json_out: Annotated[
        Path | None,
        typer.Option(
            "--json-out",
            file_okay=True,
            dir_okay=False,
            help="Write the full wiring report to this JSON file.",
        ),
    ] = None,
    print_json: Annotated[
        bool,
        typer.Option("--json", help="Print full wiring report as JSON to stdout."),
    ] = False,
) -> None:
    """Scan a monadic source tree for upward tier-import violations and auto-fix them.

    Tier rule: a1 may only import from a0; a2 from a0/a1; a3 from a0/a1/a2;
    a4 from a0-a3. Upward imports (e.g. a1 importing from a3) are violations.

    By default this command runs in **dry-run** mode — it reports violations
    and proposed patches but does not modify any file. Pass ``--apply`` to
    actually rewrite imports on disk.
    """
    # Smart default: if user passed "." and src/<pkg> exists, prefer that
    if source == Path(".").resolve() or str(source) in {".", ""}:
        cwd = Path.cwd()
        src_dir = cwd / "src"
        if src_dir.is_dir():
            subdirs = [p for p in src_dir.iterdir() if p.is_dir() and p.name.isidentifier()]
            if len(subdirs) == 1:
                source = subdirs[0]

    specialist = ContextLoaderWiringSpecialist(package_name=package_name)

    if apply:
        report = specialist.wire(source)
    else:
        context = specialist.extract_context(source)
        records = specialist.rewire_imports(source)
        fixable = [r for r in records if r.auto_fixable]
        not_fixable = [
            {"file": r.file, "file_tier": r.file_tier, "import": r.old_import,
             "imported_tier": r.imported_tier, "reason": r.reason}
            for r in records if not r.auto_fixable
        ]
        changes: dict[str, list[dict[str, str]]] = {}
        for r in fixable:
            changes.setdefault(r.file, []).append({"old": r.old_import, "new": r.new_import or ""})
        report = {
            "source_dir": str(source),
            "context": context,
            "violations_found": len(records),
            "auto_fixed": 0,
            "would_fix": len(fixable),
            "not_fixable": len(not_fixable),
            "files_changed": 0,
            "files_to_change": len(changes),
            "changes": changes,
            "manual_review": not_fixable,
            "verdict": "PASS" if not not_fixable and not fixable else ("REFINE" if not_fixable else "DRY_RUN"),
            "dry_run": True,
        }

    payload = json.dumps(report, indent=2, default=str) + "\n"
    if json_out is not None:
        json_out.parent.mkdir(parents=True, exist_ok=True)
        json_out.write_text(payload, encoding="utf-8")
        console.print(f"[green]wiring report written:[/green] {json_out}")
    if print_json:
        typer.echo(payload)
        return

    mode = "[yellow]DRY-RUN[/yellow]" if not apply else "[bold red]APPLY[/bold red]"
    console.print(f"[bold]Wire scan:[/bold] {source}  {mode}")

    table = Table(title="Wiring Report")
    table.add_column("Metric")
    table.add_column("Value", justify="right")
    table.add_row("Violations found", str(report["violations_found"]))
    if apply:
        table.add_row("Auto-fixed (applied)", str(report["auto_fixed"]))
        table.add_row("Files changed", str(report["files_changed"]))
    else:
        table.add_row("Would auto-fix", str(report.get("would_fix", 0)))
        table.add_row("Files that would change", str(report.get("files_to_change", 0)))
    table.add_row("Not auto-fixable", str(report["not_fixable"]))
    table.add_row("Verdict", str(report["verdict"]))
    console.print(table)

    manual = report.get("manual_review") or []
    if manual:
        console.print("\n[bold]Manual review required[/bold]")
        for item in manual[:10]:
            console.print(
                f"  - [cyan]{item.get('file', '?')}[/cyan] "
                f"({item.get('file_tier', '?')} → {item.get('imported_tier', '?')}): "
                f"{item.get('import', '?')}  — {item.get('reason', '')}"
            )

    changes = report.get("changes") or {}
    if changes and not apply:
        console.print("\n[bold]Proposed patches (dry-run)[/bold]")
        shown = 0
        for file_path, edits in changes.items():
            if shown >= 5:
                remaining = len(changes) - shown
                console.print(f"  [dim]... and {remaining} more files[/dim]")
                break
            console.print(f"  [cyan]{file_path}[/cyan]")
            for edit in edits[:3]:
                console.print(f"    [red]- {edit['old']}[/red]")
                console.print(f"    [green]+ {edit['new']}[/green]")
            shown += 1

    if not apply and report.get("would_fix", 0) > 0:
        console.print(
            "\n[dim]Re-run with [bold]--apply[/bold] to write these patches to disk.[/dim]"
        )
