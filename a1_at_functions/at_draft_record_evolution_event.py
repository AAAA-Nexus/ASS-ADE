# Extracted from C:/!ass-ade/src/ass_ade/protocol/evolution.py:424
# Component id: at.source.ass_ade.record_evolution_event
from __future__ import annotations

__version__ = "0.1.0"

def record_evolution_event(
    *,
    root: Path,
    event_type: str,
    summary: str,
    version: str = "",
    rebuild_path: Path | None = None,
    commands: list[EvolutionCommand] | None = None,
    metrics: dict[str, Any] | None = None,
    reports: list[str] | None = None,
    artifacts: list[str] | None = None,
    rationale: str = "",
    next_steps: list[str] | None = None,
    lineage_ids: list[str] | None = None,
    timestamp_utc: str = "",
) -> EvolutionRecordResult:
    root = root.resolve()
    timestamp = timestamp_utc or datetime.now(timezone.utc).replace(microsecond=0).isoformat()
    if timestamp.endswith("+00:00"):
        timestamp = f"{timestamp[:-6]}Z"
    version_value = version.strip() or read_project_version(root)
    event_id = _event_id(timestamp, event_type, summary)
    event = EvolutionEvent(
        event_id=event_id,
        timestamp_utc=timestamp,
        event_type=event_type,
        summary=summary,
        version=version_value,
        root=str(root),
        git=collect_git_state(root),
        commands=commands or [],
        metrics=metrics or {},
        reports=reports or [],
        artifacts=artifacts or [],
        rationale=rationale,
        next_steps=next_steps or [],
        rebuild=collect_rebuild_summary(rebuild_path),
        certificates=collect_certificate_summaries(root, rebuild_path),
        lineage_ids=lineage_ids if lineage_ids is not None else collect_lineage_ids(root),
    )

    evolution_dir = root / DEFAULT_EVOLUTION_DIR
    events_dir = root / DEFAULT_EVENTS_DIR
    ledger_path = root / DEFAULT_LEDGER_PATH
    markdown_path = root / DEFAULT_MARKDOWN_PATH
    evolution_dir.mkdir(parents=True, exist_ok=True)
    events_dir.mkdir(parents=True, exist_ok=True)
    snapshot_path = events_dir / _event_filename(timestamp, event_id)

    payload = event.model_dump(mode="json", by_alias=True)
    snapshot_path.write_text(f"{json.dumps(payload, indent=2, default=str)}\n", encoding="utf-8")
    with ledger_path.open("a", encoding="utf-8") as fh:
        fh.write(f"{json.dumps(payload, sort_keys=True, default=str)}\n")

    events = _load_ledger(root)
    markdown_path.write_text(f"{render_evolution_markdown(root, events)}\n", encoding="utf-8")
    return EvolutionRecordResult(
        event=event,
        ledger_path=str(ledger_path),
        snapshot_path=str(snapshot_path),
        markdown_path=str(markdown_path),
    )
