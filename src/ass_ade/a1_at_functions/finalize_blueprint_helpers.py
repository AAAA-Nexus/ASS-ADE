"""Tier a1 — assimilated function 'finalize_blueprint'

Assimilated from: rebuild/schema_materializer.py:1367-1486
"""

from __future__ import annotations


# --- assimilated symbol ---
def finalize_blueprint(
    rebuild_receipt: dict[str, Any],
    audit: dict[str, Any],
    *,
    forge_summary: dict[str, Any] | None = None,
    package_summary: dict[str, Any] | None = None,
    plan_summary: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Emit BLUEPRINT.json from the FINAL on-disk state of the build.

    This is the marketplace artifact: engine + blueprint + atom bodies =
    deterministic reconstruction. Run AFTER materialize, import-rewrite,
    forge, and audit so body hashes reflect the shipped state.
    """
    target_root = Path(rebuild_receipt["target_root"])
    manifest_path = target_root / "MANIFEST.json"
    if not manifest_path.is_file():
        raise FileNotFoundError(f"MANIFEST.json missing at {manifest_path}")
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    components = manifest.get("components") or []

    atoms: list[dict[str, Any]] = []
    for w in components:
        # Re-hash the body from disk so post-forge fixes are reflected.
        src_file = w.get("source_file")
        body_hash = w.get("body_hash")
        module_path = None
        if src_file:
            sp = Path(src_file)
            if sp.is_file():
                body_hash = hashlib.sha256(sp.read_bytes()).hexdigest()
            try:
                if sp.is_relative_to(target_root):
                    module_path = sp.relative_to(target_root).as_posix()
            except (AttributeError, ValueError):
                pass
        atoms.append({
            "id": w["id"],
            "tier": w["tier"],
            "name": w["name"],
            "kind": w["kind"],
            "version": w["version"],
            "body_hash": body_hash,
            "fulfills_blueprints": w.get("fulfills_blueprints", []),
            "module_path": module_path,
        })

    blueprint = {
        "blueprint_schema": "ASSADE-SPEC-BLUEPRINT-1",
        "rebuild_tag": rebuild_receipt.get("rebuild_tag"),
        "generated_at": dt.datetime.now(dt.timezone.utc).isoformat(),
        "source_plan_digest": rebuild_receipt.get("source_plan_digest"),
        "counts": manifest.get("counts", {}),
        "tier_versions": manifest.get("tier_versions", {}),
        "audit": {
            "valid": audit.get("valid"),
            "total": audit.get("total"),
            "pass_rate": audit.get("summary", {}).get("pass_rate"),
            "structure_conformant": audit.get("summary", {}).get("structure_conformant"),
        },
        "forge": {
            "applied": (forge_summary or {}).get("applied", 0),
            "tasks": (forge_summary or {}).get("tasks", 0),
        } if forge_summary else None,
        "package": {
            k: (package_summary or {}).get(k)
            for k in (
                "agents",
                "leak_patterns",
                "specs",
                "ato_plans",
                "tier_map",
                "generated_tests",
                "coverage_reports",
                "coverage_manifests",
                "bridge_reports",
                "bridge_manifests",
                "bridge_languages",
            )
        } if package_summary else None,
        "atoms": sorted(atoms, key=lambda r: (r["tier"], r["id"])),
        "plan_diff": _diff_against_plan(atoms, plan_summary) if plan_summary else None,
        "reconstruction": {
            "engine": "ass-ade>=0.1",
            "command": (
                "ass-ade rebuild-from-blueprint BLUEPRINT.json "
                "--source <atom-repo> --output ./out"
            ),
            "requires": [
                "scripts/leak_patterns/symbols.txt",
                ".ass-ade/specs/cna-seed.yaml",
            ],
            "ships_with": [
                "agents/",
                "scripts/leak_patterns/",
                ".ass-ade/specs/",
                "MANIFEST.json",
                "CERTIFICATE.json",
            ],
            "marketplace": (
                "Sell the BLUEPRINT.json on the marketplace; buyers run "
                "`ass-ade rebuild-from-blueprint` against any atom registry "
                "to reproduce the build. Body hashes verify integrity."
            ),
        },
    }
    blueprint_path = target_root / "BLUEPRINT.json"
    blob = json.dumps(blueprint, indent=2, sort_keys=True) + "\n"
    blueprint_path.write_text(blob, encoding="utf-8")
    summary = {
        "blueprint_path": blueprint_path.as_posix(),
        "blueprint_sha256": hashlib.sha256(blob.encode("utf-8")).hexdigest(),
        "atoms_total": len(atoms),
    }
    if blueprint.get("plan_diff"):
        summary["plan_diff"] = {
            k: blueprint["plan_diff"].get(k)
            for k in ("missing_count", "extra_count", "intended_count", "realized_count")
        }
    return summary

