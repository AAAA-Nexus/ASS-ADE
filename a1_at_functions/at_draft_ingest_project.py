# Extracted from C:/!ass-ade/src/ass_ade/engine/rebuild/project_parser.py:215
# Component id: at.source.ass_ade.ingest_project
from __future__ import annotations

__version__ = "0.1.0"

def ingest_project(
    source_root: Path,
    root_id: str = "source",
    *,
    registry: list[dict[str, Any]] | None = None,
    emit_drafts: bool = False,
    draft_dir: Path | None = None,
    progress_callback: "Any | None" = None,
) -> dict[str, Any]:
    """Scan ``source_root`` and return an ingestion report dict.

    Args:
        source_root: Directory to scan.
        root_id: Logical identifier for this project root.
        registry: Optional list of existing component specs for registry matching.
        emit_drafts: Write draft JSON files for each gap.
        draft_dir: Where to write draft files (only used when ``emit_drafts`` is True).
        progress_callback: Optional callable(current, total) called per file processed.
    """
    registry = registry or []
    symbols: list[Symbol] = []
    all_files = list(iter_source_files(source_root))
    total_files = len(all_files)
    for idx, path in enumerate(all_files, 1):
        symbols.extend(extract_symbols(path))
        if progress_callback is not None:
            try:
                progress_callback(idx, total_files)
            except Exception:
                pass

    candidates = [classify_symbol(s, root_id, registry) for s in symbols]
    gaps = [c for c in candidates if c["status"] == "gap"]
    draft_paths: list[str] = []
    if emit_drafts and draft_dir is not None:
        draft_paths = _emit_draft_components(gaps, root_id, draft_dir)

    by_tier: dict[str, int] = {}
    for c in candidates:
        tier = c["tier"]
        by_tier[tier] = by_tier.get(tier, 0) + 1

    files_scanned = total_files
    return {
        "ingestion_schema": INGESTION_SCHEMA,
        "generated_at": dt.datetime.now(dt.timezone.utc).isoformat(),
        "source_root": source_root.as_posix(),
        "root_id": root_id,
        "mode": "draft-components" if emit_drafts else "report-only",
        "summary": {
            "files_scanned": files_scanned,
            "symbols": len(symbols),
            "candidate_components": len(candidates),
            "mapped": sum(1 for c in candidates if c["status"] == "mapped"),
            "gaps": len(gaps),
            "drafts_written": len(draft_paths),
            "by_tier": by_tier,
        },
        "symbols": [asdict(s) for s in symbols],
        "candidate_components": candidates,
        "gaps": gaps,
        "draft_paths": draft_paths,
    }
