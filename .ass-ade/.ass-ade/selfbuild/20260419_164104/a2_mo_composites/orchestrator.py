"""Standalone Rebuild Orchestrator.

Full 7-phase pipeline:
  0. Recon        — quick stats (delegated to ass_ade.recon if available)
  1. Ingest       — scan source, classify symbols to tiers
  2. Gap-Fill     — build component proposals
  3. Enrich       — attach source bodies + derive made_of graph
  4. Validate     — enforce cycle-free tier purity
  5. Materialize  — write tier-partitioned draft folder (whole modules)
  6. Audit        — self-lint the materialized folder
  7. Package      — emit __init__.py + pyproject.toml

No external ecosystem dependency. Everything runs from this package.
"""

from __future__ import annotations

import datetime as dt
import json
from pathlib import Path
from typing import Any, Union

from ass_ade.engine.rebuild.body_extractor import derive_made_of_graph, enrich_components_with_bodies
from ass_ade.engine.rebuild.cycle_detector import break_cycles, detect_cycles
from ass_ade.engine.rebuild.gap_filler import build_gap_fill_plan
from ass_ade.engine.rebuild.package_emitter import emit_agent_configs, emit_runnable_package, emit_tier_map
from ass_ade.engine.rebuild.project_parser import ingest_project
from ass_ade.engine.rebuild.schema_materializer import emit_certificate, materialize_plan, validate_rebuild
from ass_ade.engine.rebuild.synthesis import synthesize_missing_components
from ass_ade.engine.rebuild.tier_purity import enforce_tier_purity


def _merge_by_tier(by_tier_list: list[dict[str, int]]) -> dict[str, int]:
    merged: dict[str, int] = {}
    for by_tier in by_tier_list:
        for tier, count in by_tier.items():
            merged[tier] = merged.get(tier, 0) + count
    return merged


def rebuild_project(
    source_path: Union[Path, list[Path]],
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
    # Output package
    package_name: str = "ass_ade_rebuild",
    # Rebuild tag
    rebuild_tag: str | None = None,
) -> dict[str, Any]:
    """Run the full rebuild pipeline on one or more source paths.

    Args:
        source_path:  Single directory or list of directories to scan and merge.
                      When multiple paths are given their symbol pools are merged
                      before classification; newer sources (by mtime) win on
                      dedup_key conflicts.
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
    if isinstance(source_path, (str, Path)):
        source_paths: list[Path] = [Path(source_path).resolve()]
    else:
        source_paths = [Path(p).resolve() for p in source_path]

    source_paths.sort(
        key=lambda p: p.stat().st_mtime if p.exists() else 0.0,
        reverse=True,
    )

    output_dir = Path(output_dir).resolve()
    output_dir.mkdir(parents=True, exist_ok=True)

    started_at = dt.datetime.now(dt.timezone.utc).isoformat()
    phases: dict[str, Any] = {}

    # ── Phase 1: Ingest ───────────────────────────────────────────────────────
    ingestions: list[dict[str, Any]] = []
    for sp in source_paths:
        ingestion = ingest_project(sp, root_id=sp.name, registry=registry or [])
        ingestions.append(ingestion)

    phases["ingest"] = {
        "source_roots": [i["source_root"] for i in ingestions],
        "source_root": ingestions[0]["source_root"] if len(ingestions) == 1 else None,
        "files_scanned": sum(i["summary"]["files_scanned"] for i in ingestions),
        "symbols": sum(i["summary"]["symbols"] for i in ingestions),
        "gaps": sum(i["summary"]["gaps"] for i in ingestions),
        "mapped": sum(i["summary"]["mapped"] for i in ingestions),
        "by_tier": _merge_by_tier([i["summary"]["by_tier"] for i in ingestions]),
    }

    # ── Phase 2: Gap-Fill ─────────────────────────────────────────────────────
    gap_plan = build_gap_fill_plan(
        ingestions,
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
    receipt = materialize_plan(gap_plan, out_dir=output_dir, rebuild_tag=rebuild_tag, package_name=package_name)
    phases["materialize"] = {
        "target_root": receipt["target_root"],
        "written_count": receipt["written_count"],
        "by_tier": receipt["by_tier"],
        "rebuild_tag": receipt["rebuild_tag"],
        "written_modules": len(receipt.get("written_modules", [])),
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
        primary_source = source_paths[0] if source_paths else None
        try:
            pkg = emit_runnable_package(
                target_root,
                package_name=package_name,
                control_root=output_dir,
                source_root=primary_source,
            )
            phases["package"] = {
                "importable": pkg["importable"],
                "pyproject": pkg["pyproject"],
                "init_files": len(pkg["init_files"]),
            }
        except Exception as exc:  # noqa: BLE001
            phases["package"] = {"error": str(exc)}

    # ── Phase 8: Layout Synthesis ─────────────────────────────────────────────
    layout_result: dict[str, Any] = {}
    tier_map = receipt.get("tier_map", {})
    try:
        tier_map_path = emit_tier_map(
            target_root,
            tier_map,
            package_name=package_name,
            control_root=output_dir,
        )
        layout_result["tier_map"] = tier_map_path
        layout_result["tier_map_entries"] = len(tier_map)
    except Exception as exc:  # noqa: BLE001
        layout_result["tier_map_error"] = str(exc)
    try:
        agent_configs = emit_agent_configs(
            target_root,
            package_name=package_name,
            control_root=output_dir,
        )
        layout_result["agent_configs"] = agent_configs
    except Exception as exc:  # noqa: BLE001
        layout_result["agent_configs_error"] = str(exc)
    layout_result["src_layout_root"] = receipt.get("src_layout_root")
    phases["layout_synthesis"] = layout_result

    primary_source = source_paths[0] if source_paths else output_dir
    return {
        "rebuild_schema": "ASSADE-SPEC-REBUILD-1",
        "generated_at": started_at,
        "source_path": primary_source.as_posix(),
        "source_paths": [p.as_posix() for p in source_paths],
        "output_dir": output_dir.as_posix(),
        "phases": phases,
    }


def render_rebuild_summary(result: dict[str, Any]) -> str:
    """Return a human-readable rebuild summary for CLI display."""
    phases = result.get("phases", {})
    ingest = phases.get("ingest", {})
    gap = phases.get("gap_fill", {})
    mat = phases.get("materialize", {})
    audit = phases.get("audit", {})
    cert = phases.get("certificate", {})
    pkg = phases.get("package", {})
    cycles = phases.get("cycles", {})
    purity = phases.get("tier_purity", {})
    layout = phases.get("layout_synthesis", {})

    lines: list[str] = [
        f"[Phase 1] Ingest     : {ingest.get('files_scanned', 0)} files, "
        f"{ingest.get('symbols', 0)} symbols, {ingest.get('gaps', 0)} gaps",
        f"[Phase 2] Gap-Fill   : {gap.get('proposed_components', 0)} proposals",
    ]
    if phases.get("enrich"):
        e = phases["enrich"]
        lines.append(f"[Phase 3] Enrich     : {e.get('bodies_attached', 0)} bodies, "
                     f"{e.get('made_of_edges', 0)} edges")
    if cycles.get("cycle_count"):
        lines.append(f"[Phase 4] Cycles     : {cycles['cycle_count']} detected + broken")
    else:
        lines.append("[Phase 4] Cycles     : none (acyclic)")
    if purity.get("removed_edges"):
        lines.append(f"[Phase 4] Purity     : {purity['removed_edges']} violating edges removed")
    lines.append(
        f"[Phase 5] Materialize: {mat.get('written_count', 0)} components "
        f"({mat.get('written_modules', 0)} modules) -> {mat.get('target_root', '')}"
    )
    pass_rate = audit.get("pass_rate", 0.0)
    lines.append(
        f"[Phase 6] Audit      : {audit.get('valid', 0)}/{audit.get('total', 0)} clean "
        f"({pass_rate * 100:.1f}%), "
        f"{'conformant' if audit.get('structure_conformant') else 'non-conformant'}"
    )
    if cert.get("certificate_sha256"):
        lines.append(
            f"[Cert]    SHA-256    : {cert['certificate_sha256'][:16]}..."
        )
    if pkg.get("importable"):
        lines.append(f"[Phase 7] Package    : pip install -e {mat.get('target_root', '')}")
    elif pkg.get("error"):
        lines.append(f"[Phase 7] Package    : error — {pkg['error']}")
    if layout.get("tier_map"):
        lines.append(
            f"[Phase 8] Layout     : {layout.get('tier_map_entries', 0)} files in tier-map"
            + (f", src={layout['src_layout_root']}" if layout.get("src_layout_root") else "")
        )
    elif layout.get("tier_map_error"):
        lines.append(f"[Phase 8] Layout     : error — {layout['tier_map_error']}")

    return "\n".join(lines)
