# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a1_at_functions/at_draft_rebuild_project.py:7
# Component id: at.source.a1_at_functions.rebuild_project
from __future__ import annotations

__version__ = "0.1.0"

def rebuild_project(
    source_path: Path,
    output_dir: Path,
    *,
    # Phase options
    enrich_bodies: bool = True,
    break_cycles_if_found: bool = True,
    enforce_purity: bool = True,
    emit_package: bool = True,
    synthesize_gaps: bool = False,
    # Registry / blueprints
    registry: list[dict[str, Any]] | None = None,
    blueprints: list[dict[str, Any]] | None = None,
    # Synthesis (requires Nexus credentials)
    nexus_base_url: str | None = None,
    nexus_api_key: str | None = None,
    nexus_agent_id: str | None = None,
    max_synthesize: int = 50,
    # Rebuild tag
    rebuild_tag: str | None = None,
) -> dict[str, Any]:
    """Run the full rebuild pipeline on ``source_path``.

    Args:
        source_path:  Directory to scan and rebuild.
        output_dir:   Parent directory for the timestamped rebuild folder.
                      A subfolder ``<tag>`` is created under it.
        enrich_bodies:         Extract source bodies + derive call-graph edges.
        break_cycles_if_found: Remove dependency cycles automatically.
        enforce_purity:        Strip tier-law-violating edges.
        emit_package:          Write ``__init__.py`` + ``pyproject.toml``.
        synthesize_gaps:       Synthesize missing blueprint components via Nexus.
        registry:              Optional pre-built component registry for gap matching.
        blueprints:            Optional list of blueprint dicts for fulfillment tracking.
        nexus_base_url:        Nexus endpoint for synthesis / enrichment.
        nexus_api_key:         API key for Nexus calls.
        nexus_agent_id:        Agent id for Nexus calls.
        max_synthesize:        Cap on synthesized components per run.
        rebuild_tag:           Override the auto-generated timestamp tag.

    Returns:
        A receipt dict containing per-phase summaries and paths.
    """
    source_path = Path(source_path).resolve()
    output_dir = Path(output_dir).resolve()
    output_dir.mkdir(parents=True, exist_ok=True)

    started_at = dt.datetime.now(dt.timezone.utc).isoformat()
    phases: dict[str, Any] = {}

    # ── Phase 1: Ingest ───────────────────────────────────────────────────────
    ingestion = ingest_project(
        source_path,
        root_id=source_path.name,
        registry=registry or [],
    )
    phases["ingest"] = {
        "source_root": ingestion["source_root"],
        "files_scanned": ingestion["summary"]["files_scanned"],
        "symbols": ingestion["summary"]["symbols"],
        "gaps": ingestion["summary"]["gaps"],
        "mapped": ingestion["summary"]["mapped"],
        "by_tier": ingestion["summary"]["by_tier"],
    }

    # ── Phase 2: Gap-Fill ─────────────────────────────────────────────────────
    gap_plan = build_gap_fill_plan(
        [ingestion],
        blueprints=blueprints or [],
        registry=registry or [],
    )
    phases["gap_fill"] = {
        "proposed_components": gap_plan["summary"].get("proposed_components", 0),
        "by_tier": gap_plan["summary"].get("by_tier", {}),
        "blueprints_assessed": gap_plan["summary"].get("blueprints_assessed", 0),
        "blueprints_fully_satisfied": gap_plan["summary"].get("blueprints_fully_satisfied", 0),
        "content_digest": gap_plan.get("content_digest"),
    }

    # ── Phase 3: Enrich ───────────────────────────────────────────────────────
    if enrich_bodies:
        enrich_components_with_bodies(gap_plan)
        derive_made_of_graph(gap_plan)
        bodies_attached = sum(
            1 for p in gap_plan.get("proposed_components", []) if p.get("body")
        )
        total_edges = sum(
            len(p.get("made_of", [])) for p in gap_plan.get("proposed_components", [])
        )
        phases["enrich"] = {"bodies_attached": bodies_attached, "made_of_edges": total_edges}

    # ── Phase 3b: Synthesize (optional) ──────────────────────────────────────
    if synthesize_gaps:
        import os as _os
        synth_receipt = synthesize_missing_components(
            gap_plan,
            base_url=nexus_base_url or _os.environ.get("AAAA_NEXUS_BASE_URL", "https://atomadic.tech"),
            api_key=nexus_api_key or _os.environ.get("AAAA_NEXUS_API_KEY"),
            agent_id=nexus_agent_id or _os.environ.get("AAAA_NEXUS_AGENT_ID"),
            max_synthesize=max_synthesize,
        )
        phases["synthesis"] = synth_receipt

    # ── Phase 4a: Cycle detection ─────────────────────────────────────────────
    cycle_report = detect_cycles(gap_plan)
    phases["cycles"] = {
        "cycle_count": cycle_report["cycle_count"],
        "nodes_in_cycles": cycle_report["nodes_in_cycles"],
        "acyclic": cycle_report["acyclic"],
    }
    if not cycle_report["acyclic"] and break_cycles_if_found:
        break_receipt = break_cycles(gap_plan, cycle_report)
        phases["cycles"]["break_receipt"] = break_receipt

    # ── Phase 4b: Tier purity ─────────────────────────────────────────────────
    if enforce_purity:
        purity_receipt = enforce_tier_purity(gap_plan)
        phases["tier_purity"] = purity_receipt

    # ── Phase 5: Materialize ──────────────────────────────────────────────────
    receipt = materialize_plan(gap_plan, out_dir=output_dir, rebuild_tag=rebuild_tag)
    phases["materialize"] = {
        "target_root": receipt["target_root"],
        "written_count": receipt["written_count"],
        "by_tier": receipt["by_tier"],
        "rebuild_tag": receipt["rebuild_tag"],
    }

    # ── Phase 6: Audit ────────────────────────────────────────────────────────
    target_root = Path(receipt["target_root"])
    audit = validate_rebuild(target_root)
    receipt["source_plan_digest"] = gap_plan.get("content_digest")
    phases["audit"] = {
        "total": audit["total"],
        "valid": audit["valid"],
        "pass_rate": audit.get("summary", {}).get("pass_rate", 0.0),
        "structure_conformant": audit.get("summary", {}).get("structure_conformant", False),
        "findings_total": audit.get("summary", {}).get("findings_total", 0),
    }

    # ── Certificate ───────────────────────────────────────────────────────────
    certificate = emit_certificate(receipt, audit)
    phases["certificate"] = certificate

    # ── Phase 7: Package ──────────────────────────────────────────────────────
    if emit_package:
        try:
            pkg = emit_runnable_package(target_root, control_root=output_dir)
            phases["package"] = {
                "importable": pkg["importable"],
                "pyproject": pkg["pyproject"],
                "init_files": len(pkg["init_files"]),
            }
        except Exception as exc:  # noqa: BLE001
            phases["package"] = {"error": str(exc)}

    return {
        "rebuild_schema": "ASSADE-SPEC-REBUILD-1",
        "generated_at": started_at,
        "source_path": source_path.as_posix(),
        "output_dir": output_dir.as_posix(),
        "phases": phases,
    }
