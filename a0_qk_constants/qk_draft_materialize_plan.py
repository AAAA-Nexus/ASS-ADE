# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a0_qk_constants/qk_draft_materialize_plan.py:7
# Component id: qk.source.a0_qk_constants.materialize_plan
from __future__ import annotations

__version__ = "0.1.0"

def materialize_plan(
    plan: dict[str, Any],
    *,
    out_dir: Path,
    rebuild_tag: str | None = None,
    prev_manifest_path: Path | None = None,
) -> dict[str, Any]:
    """Write every proposed component in ``plan`` as a JSON (+ optional source) file.

    Returns a materialization receipt with paths, tier distribution, tier versions,
    and a pointer to the rebuild folder.

    Args:
        plan:               Gap-fill plan from ``gap_filler.build_gap_fill_plan``.
        out_dir:            Parent directory for the timestamped rebuild folder.
        rebuild_tag:        Optional timestamp tag; auto-generated when omitted.
        prev_manifest_path: MANIFEST.json from a previous build for version continuity.
                            When provided, module versions are bumped based on API diffs.
                            When omitted, all modules start at 0.1.0.
    """
    tag = rebuild_tag or dt.datetime.now().strftime("%Y%m%d_%H%M%S")
    target_root = out_dir / tag
    _assert_under_root(target_root, out_dir)
    target_root.mkdir(parents=True, exist_ok=True)

    prev_versions = load_prev_versions(prev_manifest_path)

    written: list[dict[str, Any]] = []
    by_tier: dict[str, int] = {}
    tier_module_versions: dict[str, list[dict[str, Any]]] = {}

    for proposal in plan.get("proposed_components") or []:
        tier = proposal.get("tier") or "a1_at_functions"
        prefix = TIER_PREFIX.get(tier, "at")
        tier_dir = target_root / tier
        tier_dir.mkdir(parents=True, exist_ok=True)
        name_slug = _slug(proposal.get("name") or "component")
        file_path = tier_dir / f"{prefix}_draft_{name_slug}.json"
        _assert_under_root(file_path, out_dir)

        artifact = _make_component_artifact(proposal)

        src_sym = proposal.get("source_symbol") or {}
        body = proposal.get("body") or ""
        lang = (src_sym.get("language") or "python").lower()

        version, change_type = assign_version(artifact["id"], body, lang, prev_versions)
        artifact["version"] = version
        artifact["body_hash"] = content_hash(body)
        if change_type == "major":
            artifact["compat_warning"] = "public API removed or renamed — review before shipping"

        file_path.write_text(
            json.dumps(artifact, indent=2, sort_keys=True) + "\n", encoding="utf-8"
        )

        tier_module_versions.setdefault(tier, []).append({
            "id": artifact["id"],
            "name": artifact["name"],
            "version": version,
            "change_type": change_type,
        })

        sibling_emitted: str | None = None
        if body:
            suffix = {"python": ".py", "typescript": ".ts", "rust": ".rs"}.get(lang, ".txt")
            src_file = tier_dir / f"{prefix}_draft_{name_slug}{suffix}"
            _assert_under_root(src_file, out_dir)
            if suffix == ".py":
                header = (
                    f"# Extracted from {src_sym.get('path', '?')}:{src_sym.get('line', 0)}\n"
                    f"# Component id: {artifact['id']}\n"
                    f"__version__ = \"{version}\"\n\n"
                )
            else:
                header = (
                    f"// Extracted from {src_sym.get('path', '?')}:{src_sym.get('line', 0)}\n"
                    f"// Component id: {artifact['id']}  version: {version}\n\n"
                )
            src_file.write_text(header + body, encoding="utf-8")
            sibling_emitted = src_file.as_posix()

        written.append({
            "body_hash": artifact["body_hash"],
            "change_type": change_type,
            "fulfills_blueprints": artifact["fulfills_blueprints"],
            "id": artifact["id"],
            "kind": artifact["kind"],
            "name": artifact["name"],
            "path": file_path.as_posix(),
            "source_file": sibling_emitted,
            "tier": tier,
            "version": version,
        })
        by_tier[tier] = by_tier.get(tier, 0) + 1

    # Write per-tier VERSION.json files
    tier_versions: dict[str, str] = {}
    for tier, modules in tier_module_versions.items():
        tier_dir = target_root / tier
        write_tier_version_file(tier_dir, tier, modules)
        from ass_ade.engine.rebuild.version_tracker import _aggregate_version  # noqa: PLC0415
        tier_versions[tier] = _aggregate_version([m["version"] for m in modules])

    # Write root VERSION file
    write_project_version_file(target_root, tier_versions, tag)

    manifest_path = target_root / "MANIFEST.json"
    _assert_under_root(manifest_path, out_dir)
    manifest = {
        "schema": COMPONENT_SCHEMA,
        "rebuild_tag": tag,
        "materialized_at": dt.datetime.now(dt.timezone.utc).isoformat(),
        "source_plan_digest": plan.get("content_digest"),
        "counts": {"total": len(written), "by_tier": by_tier},
        "tier_versions": tier_versions,
        "components": written,
    }
    manifest_path.write_text(
        json.dumps(manifest, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )

    pointer = out_dir / "latest.txt"
    _assert_under_root(pointer, out_dir)
    pointer.write_text(target_root.as_posix() + "\n", encoding="utf-8")

    return {
        "rebuild_tag": tag,
        "target_root": target_root.as_posix(),
        "manifest_path": manifest_path.as_posix(),
        "pointer": pointer.as_posix(),
        "written_count": len(written),
        "by_tier": by_tier,
        "tier_versions": tier_versions,
    }
