# Extracted from C:/!ass-ade/.claude/worktrees/beautiful-dubinsky-c2cb48/a1_at_functions/at_draft_protocol_evolution_record.py:5
# Component id: at.source.ass_ade.protocol_evolution_record
__version__ = "0.1.0"

def protocol_evolution_record(
    event_type: str = typer.Argument(..., help="Evolution event type, such as birth, iteration, merge, or release."),
    summary: str = typer.Option(..., "--summary", help="Public-safe summary of what changed."),
    config: Path | None = CONFIG_OPTION,
    path: Path = REPO_PATH_OPTION,
    version: str = typer.Option("", "--version", help="Version to record. Defaults to the project version."),
    rebuild_path: Path | None = typer.Option(None, "--rebuild-path", help="Optional rebuild output folder to summarize."),
    command: list[str] = typer.Option(
        [],
        "--command",
        "-c",
        help="Command receipt. Prefix with status=passed:: if useful.",
    ),
    metric: list[str] = typer.Option([], "--metric", help="Metric in key=value form. Repeatable."),
    report: list[Path] = typer.Option([], "--report", help="Report path to record. Repeatable."),
    artifact: list[Path] = typer.Option([], "--artifact", help="Artifact path to record. Repeatable."),
    rationale: str = typer.Option("", "--rationale", help="Brief public decision summary."),
    next_step: list[str] = typer.Option([], "--next-step", help="Next step to record. Repeatable."),
    lineage_id: list[str] = typer.Option([], "--lineage-id", help="Optional Nexus lineage id. Repeatable."),
    json_out: bool = typer.Option(False, "--json", help="Output raw JSON."),
) -> None:
    """Append a public-safe evolution event and refresh EVOLUTION.md."""
    _resolve_config(config)
    try:
        commands = parse_command_specs(command)
        metrics = parse_metrics(metric)
    except ValueError as exc:
        console.print(f"[red]Evolution record error:[/red] {exc}")
        raise typer.Exit(code=4) from exc

    result = record_evolution_event(
        root=path,
        event_type=event_type,
        summary=summary,
        version=version,
        rebuild_path=rebuild_path,
        commands=commands,
        metrics=metrics,
        reports=[str(item) for item in report],
        artifacts=[str(item) for item in artifact],
        rationale=rationale,
        next_steps=next_step,
        lineage_ids=lineage_id or None,
    )

    if json_out:
        _print_json(result.model_dump(), redact=True)
        return

    table = Table(title="Evolution Event Recorded")
    table.add_column("Signal")
    table.add_column("Value")
    table.add_row("Event", result.event.event_type)
    table.add_row("Event ID", result.event.event_id)
    table.add_row("Version", result.event.version)
    table.add_row("Ledger", result.ledger_path)
    table.add_row("Snapshot", result.snapshot_path)
    table.add_row("Markdown", result.markdown_path)
    console.print(table)
