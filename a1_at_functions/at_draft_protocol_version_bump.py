# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a1_at_functions/at_draft_protocol_version_bump.py:7
# Component id: at.source.a1_at_functions.protocol_version_bump
from __future__ import annotations

__version__ = "0.1.0"

def protocol_version_bump(
    bump: str = typer.Argument(..., help="patch, minor, or major. Use --to for an explicit version."),
    path: Path = REPO_PATH_OPTION,
    to_version: str = typer.Option("", "--to", help="Explicit semantic version to set."),
    summary: str = typer.Option("Version update", "--summary", help="Release note summary."),
    dry_run: bool = typer.Option(False, "--dry-run", help="Preview without writing files or ledger entries."),
    json_out: bool = typer.Option(False, "--json", help="Output raw JSON."),
) -> None:
    """Update package version surfaces and record the bump in the evolution ledger."""
    try:
        bump_result = bump_project_version(
            root=path,
            bump=bump,
            new_version=to_version,
            summary=summary,
            dry_run=dry_run,
        )
    except ValueError as exc:
        console.print(f"[red]Version bump error:[/red] {exc}")
        raise typer.Exit(code=4) from exc

    event_result = None
    if not dry_run:
        command_text = f"status=completed::ass-ade protocol version-bump {bump}"
        if to_version:
            command_text = f"{command_text} --to {to_version}"
        event_result = record_evolution_event(
            root=path,
            event_type="version-bump",
            summary=summary,
            version=bump_result.new_version,
            commands=parse_command_specs([command_text]),
            metrics={
                "old_version": bump_result.old_version,
                "new_version": bump_result.new_version,
            },
            artifacts=bump_result.files_updated,
            rationale="Package version surfaces were updated together before release.",
        )

    payload = {
        "version": bump_result.model_dump(),
        "event": event_result.model_dump() if event_result is not None else None,
    }
    if json_out:
        _print_json(payload, redact=True)
        return

    console.print(
        f"[green]Version:[/green] {bump_result.old_version} -> {bump_result.new_version}"
        + (" (dry run)" if dry_run else "")
    )
    for item in bump_result.files_updated:
        console.print(f"  - {item}")
    if event_result is not None:
        console.print(f"[green]Evolution event:[/green] {event_result.event.event_id}")
