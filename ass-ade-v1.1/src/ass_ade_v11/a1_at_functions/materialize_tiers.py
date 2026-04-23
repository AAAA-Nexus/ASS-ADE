"""Materialize enriched gap plan to tier directories (.py + JSON sidecars)."""

from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path
from typing import Any

from ass_ade_v11.a0_qk_constants.schemas import ASSIMILATION_LOG_SCHEMA, COMPONENT_SCHEMA_V11
from ass_ade_v11.a0_qk_constants.tier_names import VALID_TIER_DIRS
from ass_ade_v11.a1_at_functions.cna_import_rewrite import assimilate_component_body


def _stem_from_id(cid: str) -> str:
    s = re.sub(r"[^a-zA-Z0-9._]+", "_", cid.strip())
    return s.replace(".", "_") or "component"


def materialize_gap_plan_to_tree(
    gap_plan: dict[str, Any],
    output_parent: Path,
    rebuild_tag: str,
    *,
    write_json_sidecars: bool = True,
    source_roots: list[Path] | None = None,
    rewrite_imports: bool = True,
) -> dict[str, Any]:
    """Write bodies into ``output_parent / rebuild_tag / <tier>/*.py`` (+ optional .json)."""
    output_parent = output_parent.resolve()
    target_root = output_parent / rebuild_tag
    target_root.mkdir(parents=True, exist_ok=True)

    written_modules: list[str] = []
    by_tier: dict[str, int] = {}
    manifest: dict[str, str] = {}
    import_rewrite_receipts: list[dict[str, Any]] = []
    roots = [Path(p).resolve() for p in (source_roots or [])]

    for prop in gap_plan.get("proposed_components") or []:
        body = prop.get("body")
        if not body:
            continue
        tier = str(prop.get("tier") or "a1_at_functions")
        if tier not in VALID_TIER_DIRS:
            continue
        cid = str(prop.get("id") or "")
        if not cid:
            continue
        stem = _stem_from_id(cid)
        tdir = target_root / tier
        tdir.mkdir(parents=True, exist_ok=True)

        py_path = tdir / f"{stem}.py"
        body_str = str(body)
        if rewrite_imports and roots:
            body_str, ir = assimilate_component_body(
                body_str,
                dict(prop),
                gap_plan=gap_plan,
                source_roots=roots,
            )
            import_rewrite_receipts.append({"id": cid, "receipt": ir})
        py_path.write_text(body_str, encoding="utf-8")
        rel_py = py_path.relative_to(target_root).as_posix()
        manifest[rel_py] = hashlib.sha256(body_str.encode("utf-8")).hexdigest()
        written_modules.append(py_path.as_posix())
        by_tier[tier] = by_tier.get(tier, 0) + 1

        if write_json_sidecars:
            json_path = tdir / f"{stem}.json"
            sidecar: dict[str, Any] = {
                "component_schema": COMPONENT_SCHEMA_V11,
                "id": cid,
                "tier": tier,
                "name": str(prop.get("name") or ""),
                "kind": str(prop.get("kind") or ""),
                "description": str(prop.get("description") or ""),
                "made_of": list(prop.get("made_of") or []),
                "provides": list(prop.get("provides") or []),
                "reuse_policy": str(prop.get("reuse_policy") or "synthesize"),
                "status": "draft",
            }
            raw = json.dumps(sidecar, indent=2, sort_keys=True) + "\n"
            json_path.write_text(raw, encoding="utf-8")
            rel_j = json_path.relative_to(target_root).as_posix()
            manifest[rel_j] = hashlib.sha256(raw.encode("utf-8")).hexdigest()

    return {
        "target_root": target_root.as_posix(),
        "rebuild_tag": rebuild_tag,
        "written_count": len(written_modules),
        "by_tier": by_tier,
        "written_modules": written_modules,
        "content_digest": gap_plan.get("content_digest"),
        "manifest_sha256": hashlib.sha256(
            json.dumps(manifest, sort_keys=True).encode("utf-8")
        ).hexdigest(),
        "import_rewrite": import_rewrite_receipts if roots and rewrite_imports else [],
    }


def emit_plan_blueprint_v11(
    gap_plan: dict[str, Any],
    output_parent: Path,
    rebuild_tag: str,
) -> dict[str, Any]:
    """Write ``BLUEPRINT.json`` intended-state snapshot (MAP) before full materialize."""
    output_parent = output_parent.resolve()
    target_root = output_parent / rebuild_tag
    target_root.mkdir(parents=True, exist_ok=True)
    props = gap_plan.get("proposed_components") or []
    blueprint = {
        "schema": "ASSADE-BLUEPRINT-V11",
        "rebuild_tag": rebuild_tag,
        "intended_count": len(props),
        "content_digest": gap_plan.get("content_digest"),
        "components": [
            {
                "id": p.get("id"),
                "tier": p.get("tier"),
                "name": p.get("name"),
                "dedup_key": p.get("dedup_key"),
            }
            for p in props
        ],
    }
    raw = json.dumps(blueprint, indent=2, sort_keys=True) + "\n"
    path = target_root / "BLUEPRINT.json"
    path.write_text(raw, encoding="utf-8")
    sha = hashlib.sha256(raw.encode("utf-8")).hexdigest()
    return {
        "plan_blueprint_path": path.as_posix(),
        "plan_blueprint_sha256": sha,
        "intended_count": len(props),
    }


def emit_assimilation_log_v11(
    assimilation_meta: dict[str, Any],
    output_parent: Path,
    rebuild_tag: str,
) -> dict[str, Any]:
    """Write ``ASSIMILATION.json`` — provenance for multi-source merged builds."""
    output_parent = Path(output_parent).resolve()
    target_root = output_parent / rebuild_tag
    target_root.mkdir(parents=True, exist_ok=True)
    payload = {**assimilation_meta, "assimilation_schema": ASSIMILATION_LOG_SCHEMA}
    raw = json.dumps(payload, indent=2, sort_keys=True, default=str) + "\n"
    path = target_root / "ASSIMILATION.json"
    path.write_text(raw, encoding="utf-8")
    sha = hashlib.sha256(raw.encode("utf-8")).hexdigest()
    return {
        "assimilation_path": path.as_posix(),
        "assimilation_sha256": sha,
        "bytes": len(raw.encode("utf-8")),
    }
