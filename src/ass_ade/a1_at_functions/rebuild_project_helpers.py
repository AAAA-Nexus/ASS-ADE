"""Tier a1 — assimilated function 'rebuild_project'

Assimilated from: rebuild/orchestrator.py:126-488
"""

from __future__ import annotations


# --- assimilated symbol ---
def rebuild_project(
    source_path: Union[Path, list[Path]],
    output_dir: Path,
    *,
    # Phase options
    enrich_bodies: bool = True,
    break_cycles_if_found: bool = True,
    enforce_purity: bool = True,
    emit_package: bool = True,
    package_copy_dotenv: bool = True,
    synthesize_gaps: bool = False,
    # Forge phase (Epiphany + ForgeLoop LLM improvement)
    forge: bool = False,
    forge_model: str | None = None,
    forge_workers: int = 4,
    # Registry / blueprints
    registry: list[dict[str, Any]] | None = None,
    use_default_registry: bool = True,
    blueprints: list[dict[str, Any]] | None = None,
    # Synthesis (requires Nexus credentials)
    nexus_base_url: str | None = None,
    nexus_api_key: str | None = None,
    nexus_agent_id: str | None = None,
    max_synthesize: int = 50,
    # Rebuild tag
    rebuild_tag: str | None = None,
    # MAP = TERRAIN convergence
    max_converge_iterations: int = 3,
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
        package_copy_dotenv:   When vendoring ``src/ass_ade``, copy repo ``.env`` if present.
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
    # Ensure .env (cwd, repo, ~/.ass-ade) is loaded for Nexus + cloud keys.
    try:
        from ass_ade.env_bootstrap import load_all_dotenv

        load_all_dotenv(override=False)
    except Exception:
        pass

    if isinstance(source_path, (str, Path)):
        source_paths: list[Path] = [Path(source_path).resolve()]
    else:
        source_paths = [Path(p).resolve() for p in source_path]

    source_paths.sort(
        key=lambda p: p.stat().st_mtime if p.exists() else 0.0,
        reverse=True,
    )

    # Single ingest path → enforce MAP = TERRAIN: no mixed-tree proposals.
    single_ingest_root: Path | None = source_paths[0] if len(source_paths) == 1 else None
    provenance_meta: dict[str, Any] = {
        "ingest_mode": "single" if single_ingest_root else "multi",
        "source_paths": [p.as_posix() for p in source_paths],
    }

    output_dir = Path(output_dir).resolve()
    output_dir.mkdir(parents=True, exist_ok=True)

    started_at = dt.datetime.now(dt.timezone.utc).isoformat()
    phases: dict[str, Any] = {}

    registry_records, registry_candidates = resolve_registry_inputs(
        registry,
        use_default_registry=use_default_registry,
    )

    # ── Phase 1: Ingest ───────────────────────────────────────────────────────
    ingestions: list[dict[str, Any]] = []
    for sp in source_paths:
        ingestion = ingest_project(sp, root_id=sp.name, registry=registry_records)
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

    # ── Phase 1b: Namespace Conflict Detection ────────────────────────────────
    if len(source_paths) > 1:
        conflict_result = detect_namespace_conflicts(source_paths)
        phases["conflicts"] = conflict_result
        if not conflict_result["clean"]:
            import logging as _log
            _log.getLogger(__name__).warning(
                format_conflict_report(conflict_result)
            )

    # ── Phase 2: Gap-Fill ─────────────────────────────────────────────────────
    gap_plan = build_gap_fill_plan(
        ingestions,
        blueprints=blueprints or [],
        registry=registry_records,
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
        synth_receipt = synthesize_missing_components(
            gap_plan,
            base_url=nexus_base_url or os.environ.get("AAAA_NEXUS_BASE_URL", "https://atomadic.tech"),
            api_key=nexus_api_key or os.environ.get("AAAA_NEXUS_API_KEY"),
            agent_id=nexus_agent_id or os.environ.get("AAAA_NEXUS_AGENT_ID"),
            registry_candidates=registry_candidates,
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
    # 5a. Plan blueprint (intended state, pre-materialize — the MAP).
    _resolved_tag = rebuild_tag or dt.datetime.now(dt.timezone.utc).strftime("%Y%m%d_%H%M%S")
    plan_summary = emit_plan_blueprint(
        gap_plan,
        out_dir=output_dir,
        rebuild_tag=_resolved_tag,
        registry_candidates=registry_candidates,
    )
    phases["plan_blueprint"] = {
        "path": plan_summary["plan_blueprint_path"],
        "sha256": plan_summary["plan_blueprint_sha256"],
        "intended_count": plan_summary["intended_count"],
    }

    receipt = materialize_plan(
        gap_plan,
        out_dir=output_dir,
        rebuild_tag=_resolved_tag,
        registry_candidates=registry_candidates,
        allowed_source_root=single_ingest_root,
        provenance_meta=provenance_meta,
    )
    phases["materialize"] = {
        "target_root": receipt["target_root"],
        "written_count": receipt["written_count"],
        "by_tier": receipt["by_tier"],
        "rebuild_tag": receipt["rebuild_tag"],
        "written_modules": len(receipt.get("written_modules", [])),
    }

    # ── Phase 5b: Import Rewrite (fix broken cross-module imports after tier move) ─
    target_root = Path(receipt["target_root"])
    written_modules: dict[str, str] = receipt.get("written_modules_map", {})
    if written_modules:
        import_rw = rewrite_imports(target_root, written_modules)
        phases["import_rewrite"] = {
            "files_checked":   import_rw["files_checked"],
            "files_rewritten": import_rw["files_rewritten"],
            "total_changes":   import_rw["total_changes"],
            "stem_map":        import_rw["stem_map"],
            "rewritten":       import_rw["rewritten"],
            "skipped_syntax":  import_rw["skipped_syntax"],
        }

    # ── Phase 5c: Forge (Epiphany plan → parallel LLM fixes) ─────────────────
    if forge:
        try:
            from ass_ade.engine.rebuild.forge import run_forge_phase, _FORGE_MODEL
            _model = forge_model or _FORGE_MODEL
            forge_summary = run_forge_phase(
                target_root,
                model=_model,
                max_workers=forge_workers,
            )
            phases["forge"] = forge_summary
        except Exception as exc:  # noqa: BLE001
            phases["forge"] = {"error": str(exc), "applied": 0, "tasks": 0}

    # ── Phase 6: Audit ────────────────────────────────────────────────────────
    audit = validate_rebuild(target_root)
    receipt["source_plan_digest"] = gap_plan.get("content_digest")
    phases["audit"] = {
        "total": audit["total"],
        "valid": audit["valid"],
        "pass_rate": audit.get("summary", {}).get("pass_rate", 0.0),
        "structure_conformant": audit.get("summary", {}).get("structure_conformant", False),
        "provenance_conformant": audit.get("summary", {}).get("provenance_conformant", True),
        "findings_total": audit.get("summary", {}).get("findings_total", 0),
        "provenance": audit.get("provenance", {}),
    }

    # ── Phase 7: Package (run BEFORE blueprint so cert covers everything) ────
    package_summary: dict[str, Any] | None = None
    if emit_package:
        primary_source = source_paths[0] if source_paths else None
        vendor_repo = _resolve_vendor_repo_root(source_paths)
        try:
            pkg = emit_runnable_package(
                target_root,
                control_root=output_dir,
                source_root=primary_source,
                vendor_repo_root=vendor_repo,
                copy_dotenv=package_copy_dotenv
                and os.getenv("ASS_ADE_PACKAGE_SKIP_DOTENV", "").lower() not in ("1", "true", "yes"),
            )
            package_summary = {
                **(pkg.get("support_copies", {}) or {}),
                "generated_tests": pkg.get("generated_tests", []),
                "coverage_reports": pkg.get("coverage_reports", []),
                "coverage_manifests": pkg.get("coverage_manifests", []),
                "bridge_reports": pkg.get("bridge_reports", []),
                "bridge_manifests": pkg.get("bridge_manifests", []),
                "bridge_languages": pkg.get("bridge_languages", []),
            }
            phases["package"] = {
                "importable": pkg["importable"],
                "pyproject": pkg["pyproject"],
                "init_files": len(pkg["init_files"]),
                "vendored_ass_ade": pkg.get("vendored_ass_ade", False),
                "support_copies": pkg.get("support_copies", {}) or {},
                "generated_tests": pkg.get("generated_tests", []),
                "coverage_reports": pkg.get("coverage_reports", []),
                "coverage_manifests": pkg.get("coverage_manifests", []),
                "coverage_python_targets": pkg.get("coverage_python_targets", 0),
                "coverage_component_targets": pkg.get("coverage_component_targets", 0),
                "coverage_public_symbols": pkg.get("coverage_public_symbols", 0),
                "bridge_reports": pkg.get("bridge_reports", []),
                "bridge_manifests": pkg.get("bridge_manifests", []),
                "bridge_languages": pkg.get("bridge_languages", []),
                "bridge_ready": pkg.get("bridge_ready", False),
            }
        except Exception as exc:  # noqa: BLE001
            phases["package"] = {"error": str(exc)}

    # ── Phase 8: Blueprint (final on-disk truth, post-forge, post-package) ───
    blueprint_summary: dict[str, Any] | None = None
    converge_log: list[dict[str, Any]] = []
    for _iter in range(1, max(1, max_converge_iterations) + 1):
        try:
            blueprint_summary = finalize_blueprint(
                receipt,
                audit,
                forge_summary=phases.get("forge"),
                package_summary=package_summary,
                plan_summary=plan_summary,
            )
        except Exception as exc:  # noqa: BLE001
            blueprint_summary = None
            phases["blueprint"] = {"error": str(exc)}
            break
        diff = (blueprint_summary or {}).get("plan_diff") or {}
        missing = int(diff.get("missing_count") or 0)
        converge_log.append({
            "iteration": _iter,
            "missing": missing,
            "intended": diff.get("intended_count"),
            "realized": diff.get("realized_count"),
        })
        if missing == 0:
            break
        # MAP ≠ TERRAIN — re-materialize the missing atoms only.
        # Filter the gap_plan down to the missing canonical ids and run
        # materialize again into the SAME target_root (idempotent writes).
        intended_missing = set((blueprint_summary or {}).get("plan_diff", {}).get("missing") or [])
        if not intended_missing:
            break
        retry_plan = dict(gap_plan)
        retry_plan["proposed_components"] = [
            p for p in (gap_plan.get("proposed_components") or [])
            if canonical_name_for(
                p,
                fallback_tier=p.get("tier") or "a1_at_functions",
                registry_candidates=registry_candidates,
            ) in intended_missing
            or (p.get("canonical_name") or p.get("id")) in intended_missing
        ]
        if not retry_plan["proposed_components"]:
            break
        try:
            materialize_plan(
                retry_plan,
                out_dir=output_dir,
                rebuild_tag=_resolved_tag,
                registry_candidates=registry_candidates,
                allowed_source_root=single_ingest_root,
                provenance_meta=provenance_meta,
            )
            audit = validate_rebuild(target_root)
        except Exception as exc:  # noqa: BLE001
            converge_log[-1]["retry_error"] = str(exc)
            break
    phases["blueprint"] = blueprint_summary or phases.get("blueprint", {})
    phases["converge"] = {
        "iterations": len(converge_log),
        "converged": (blueprint_summary or {}).get("plan_diff", {}).get("missing_count", 1) == 0,
        "log": converge_log,
    }

    # ── Phase 9: Certificate (binds blueprint + audit + package + convergence) ─
    certificate = emit_certificate(receipt, audit, blueprint_summary=blueprint_summary)
    phases["certificate"] = certificate

    primary_source = source_paths[0] if source_paths else output_dir
    return {
        "rebuild_schema": "ASSADE-SPEC-REBUILD-1",
        "generated_at": started_at,
        "source_path": primary_source.as_posix(),
        "source_paths": [p.as_posix() for p in source_paths],
        "output_dir": output_dir.as_posix(),
        "phases": phases,
    }

