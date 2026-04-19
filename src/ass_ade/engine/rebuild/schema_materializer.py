"""Schema Rebuilder — materialize a gap-fill plan into a tier-partitioned folder.

Takes the plan from ``gap_filler.build_gap_fill_plan`` and writes every
proposed component's SOURCE MODULE (whole file, intact) into the correct
tier directory.  Writing whole modules instead of extracted snippets
preserves all imports, class context, and helper code so the output is
a pip-installable, runnable Python package.

Also provides:
  - ``validate_rebuild`` — structural lint of a materialized folder
  - ``emit_certificate`` — SHA-256-bound rebuild certificate
"""

from __future__ import annotations

import datetime as dt
import hashlib
import json
import re
from pathlib import Path
from typing import Any

from ass_ade.engine.rebuild.version_tracker import (
    _aggregate_version,
    assign_version,
    content_hash,
    load_prev_versions,
    write_project_version_file,
    write_tier_version_file,
)

COMPONENT_SCHEMA = "ASSADE-SPEC-003"

TIER_PREFIX: dict[str, str] = {
    "a0_qk_constants":      "qk",
    "a1_at_functions":      "at",
    "a2_mo_composites":     "mo",
    "a3_og_features":       "og",
    "a4_sy_orchestration":  "sy",
}
_VALID_TIERS = set(TIER_PREFIX.keys())

MAX_COMPOSITION_DEPTH = 23
DUPLICATE_ID_TOLERANCE = 0.01
QUALITY_FLOOR = 0.99


def _slug(value: str) -> str:
    return re.sub(r"[^a-z0-9]+", "_", value.lower()).strip("_") or "component"


def _assert_under_root(path: Path, root: Path) -> None:
    """Refuse writes outside the rebuild root (safety boundary)."""
    resolved = path.resolve()
    try:
        resolved.relative_to(root.resolve())
    except ValueError as exc:
        raise RuntimeError(
            f"Safety boundary: {resolved} is outside rebuild root {root}"
        ) from exc


def _make_component_artifact(proposal: dict[str, Any]) -> dict[str, Any]:
    tier = proposal.get("tier") or "a1_at_functions"
    prefix = TIER_PREFIX.get(tier, "at")
    cid = proposal.get("id") or f"{prefix}.rebuild.{_slug(proposal.get('name') or 'component')}"
    artifact = {
        "component_schema": COMPONENT_SCHEMA,
        "id": cid,
        "tier": tier,
        "name": proposal.get("name") or cid.split(".")[-1],
        "kind": proposal.get("kind") or "component",
        "description": proposal.get("description") or "",
        "made_of": proposal.get("made_of") or [],
        "provides": [f"rebuild candidate for {proposal.get('name', cid)}"],
        "interfaces": {
            "source": (
                f"{proposal.get('source_symbol', {}).get('path', '')}"
                f":{proposal.get('source_symbol', {}).get('line', 0)}"
            )
        },
        "product_categories": proposal.get("product_categories") or ["COR"],
        "fulfills_blueprints": proposal.get("fulfills_blueprints") or [],
        "reuse_policy": "reference-only",
        "status": "draft",
    }
    if proposal.get("body"):
        artifact["body"] = proposal["body"]
        artifact["imports"] = proposal.get("imports") or []
        artifact["callers_of"] = proposal.get("callers_of") or []
        artifact["exceptions_raised"] = proposal.get("exceptions_raised") or []
        artifact["body_truncated"] = bool(proposal.get("body_truncated"))
    return artifact


def _dominant_tier(tier_votes: dict[str, int]) -> str:
    """Return the tier with the most votes, breaking ties by tier order."""
    tier_order = list(TIER_PREFIX.keys())
    return max(
        tier_votes,
        key=lambda t: (tier_votes[t], tier_order.index(t) if t in tier_order else 99),
    )


def materialize_plan(
    plan: dict[str, Any],
    *,
    out_dir: Path,
    rebuild_tag: str | None = None,
    prev_manifest_path: Path | None = None,
) -> dict[str, Any]:
    """Write each source module (whole file) to its dominant tier directory.

    Instead of extracting individual function bodies into separate files
    (which strips imports and class context), we copy the WHOLE source file
    to the appropriate tier folder.  Multiple components from the same source
    file are deduplicated: the file is written once to the tier where most of
    its symbols land.

    JSON component-spec artifacts are still written per component for metadata
    and audit purposes.

    Args:
        plan:               Gap-fill plan from ``gap_filler.build_gap_fill_plan``.
        out_dir:            Parent directory for the timestamped rebuild folder.
        rebuild_tag:        Optional timestamp tag; auto-generated when omitted.
        prev_manifest_path: MANIFEST.json from a previous build for version continuity.
    """
    tag = rebuild_tag or dt.datetime.now().strftime("%Y%m%d_%H%M%S")
    target_root = out_dir / tag
    _assert_under_root(target_root, out_dir)
    target_root.mkdir(parents=True, exist_ok=True)

    prev_versions = load_prev_versions(prev_manifest_path)

    # ── Step 0: Determine dominant tier per source file ───────────────────────
    # Count how many components from each source file land in each tier.
    # The file goes to the tier that claims the most of its symbols.
    file_tier_votes: dict[str, dict[str, int]] = {}
    for proposal in plan.get("proposed_components") or []:
        src_sym = proposal.get("source_symbol") or {}
        src_path = src_sym.get("path") or ""
        lang = (src_sym.get("language") or "python").lower()
        if src_path and lang == "python":
            tier = proposal.get("tier") or "a1_at_functions"
            votes = file_tier_votes.setdefault(src_path, {})
            votes[tier] = votes.get(tier, 0) + 1

    file_to_tier: dict[str, str] = {
        src: _dominant_tier(votes)
        for src, votes in file_tier_votes.items()
        if votes
    }

    # ── Step 1: Copy whole source modules (one per source file) ───────────────
    # Each unique source file is written exactly once to its dominant tier dir.
    written_modules: dict[str, str] = {}  # source_path_str → written dest path
    for src_path_str, tier in sorted(file_to_tier.items()):
        src_path = Path(src_path_str)
        if not src_path.exists():
            continue
        tier_dir = target_root / tier
        tier_dir.mkdir(parents=True, exist_ok=True)

        dest_name = src_path.name
        dest_file = tier_dir / dest_name
        # Resolve name conflicts with a counter suffix
        counter = 1
        while dest_file.exists():
            dest_file = tier_dir / f"{src_path.stem}_{counter}{src_path.suffix}"
            counter += 1

        _assert_under_root(dest_file, out_dir)
        try:
            content = src_path.read_text(encoding="utf-8", errors="ignore")
        except OSError:
            continue
        dest_file.write_text(content, encoding="utf-8")
        written_modules[src_path_str] = dest_file.as_posix()

    # ── Step 2: Write JSON component-spec artifacts ───────────────────────────
    written: list[dict[str, Any]] = []
    by_tier: dict[str, int] = {}
    tier_module_versions: dict[str, list[dict[str, Any]]] = {}

    for proposal in plan.get("proposed_components") or []:
        tier = proposal.get("tier") or "a1_at_functions"
        prefix = TIER_PREFIX.get(tier, "at")
        tier_dir = target_root / tier
        tier_dir.mkdir(parents=True, exist_ok=True)
        name_slug = _slug(proposal.get("name") or "component")
        json_file = tier_dir / f"{prefix}_draft_{name_slug}.json"
        _assert_under_root(json_file, out_dir)

        artifact = _make_component_artifact(proposal)
        body = proposal.get("body") or ""
        src_sym = proposal.get("source_symbol") or {}
        lang = (src_sym.get("language") or "python").lower()

        version, change_type = assign_version(artifact["id"], body, lang, prev_versions)
        artifact["version"] = version
        artifact["body_hash"] = content_hash(body)
        if change_type == "major":
            artifact["compat_warning"] = "public API removed or renamed — review before shipping"

        json_file.write_text(
            json.dumps(artifact, indent=2, sort_keys=True) + "\n", encoding="utf-8"
        )

        tier_module_versions.setdefault(tier, []).append({
            "id": artifact["id"],
            "name": artifact["name"],
            "version": version,
            "change_type": change_type,
        })

        src_path_str = (proposal.get("source_symbol") or {}).get("path") or ""
        sibling_emitted = written_modules.get(src_path_str)

        written.append({
            "body_hash": artifact["body_hash"],
            "change_type": change_type,
            "fulfills_blueprints": artifact["fulfills_blueprints"],
            "id": artifact["id"],
            "kind": artifact["kind"],
            "name": artifact["name"],
            "path": json_file.as_posix(),
            "source_file": sibling_emitted,
            "tier": tier,
            "version": version,
        })
        by_tier[tier] = by_tier.get(tier, 0) + 1

    # ── Step 3: Write per-tier VERSION.json ───────────────────────────────────
    tier_versions: dict[str, str] = {}
    for tier, modules in tier_module_versions.items():
        tier_dir = target_root / tier
        write_tier_version_file(tier_dir, tier, modules)
        tier_versions[tier] = _aggregate_version([m["version"] for m in modules])

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
        "written_modules": list(written_modules.values()),
    }


# ── Validation ────────────────────────────────────────────────────────────────

_REQUIRED_FIELDS = (
    "component_schema", "id", "tier", "name", "kind",
    "description", "made_of", "provides", "reuse_policy", "status",
)


def validate_rebuild(target_root: Path) -> dict[str, Any]:
    """Lint every materialized component JSON under ``target_root``."""
    if not target_root.exists():
        return {
            "validated": False,
            "reason": f"target_root does not exist: {target_root}",
            "total": 0, "valid": 0, "findings": [],
        }

    findings: list[dict[str, Any]] = []
    seen_ids: dict[str, str] = {}
    total = 0
    valid = 0

    for tier_dir in target_root.iterdir():
        if not tier_dir.is_dir() or tier_dir.name not in _VALID_TIERS:
            continue
        expected_prefix = TIER_PREFIX[tier_dir.name] + "."
        for f in sorted(f for f in tier_dir.glob("*.json") if f.name != "VERSION.json"):
            total += 1
            try:
                doc = json.loads(f.read_text(encoding="utf-8"))
            except json.JSONDecodeError as exc:
                findings.append({"severity": "error", "code": "JSON_PARSE",
                                  "path": f.as_posix(), "message": str(exc)})
                continue
            file_ok = True

            for field_name in _REQUIRED_FIELDS:
                if field_name not in doc:
                    findings.append({"severity": "error", "code": "MISSING_FIELD",
                                      "path": f.as_posix(), "field": field_name})
                    file_ok = False

            tier = doc.get("tier")
            if tier not in _VALID_TIERS:
                findings.append({"severity": "error", "code": "INVALID_TIER",
                                  "path": f.as_posix(), "tier": str(tier)})
                file_ok = False

            cid = str(doc.get("id") or "")
            if tier in _VALID_TIERS and not cid.startswith(TIER_PREFIX[tier] + "."):
                findings.append({"severity": "error", "code": "TIER_PREFIX_MISMATCH",
                                  "path": f.as_posix(), "id": cid,
                                  "expected_prefix": TIER_PREFIX[tier] + "."})
                file_ok = False

            if tier != tier_dir.name:
                findings.append({"severity": "error", "code": "TIER_DIR_MISMATCH",
                                  "path": f.as_posix(),
                                  "declared_tier": str(tier),
                                  "actual_dir": tier_dir.name})
                file_ok = False

            if doc.get("component_schema") != COMPONENT_SCHEMA:
                findings.append({"severity": "warn", "code": "SCHEMA_VERSION",
                                  "path": f.as_posix(), "got": str(doc.get("component_schema"))})

            if not isinstance(doc.get("made_of"), list):
                findings.append({"severity": "error", "code": "MADE_OF_NOT_LIST",
                                  "path": f.as_posix()})
                file_ok = False

            if cid and cid in seen_ids and seen_ids[cid] != f.as_posix():
                findings.append({"severity": "warn", "code": "DUPLICATE_ID",
                                  "path": f.as_posix(), "other": seen_ids[cid], "id": cid})
            elif cid:
                seen_ids[cid] = f.as_posix()

            if file_ok:
                valid += 1

    structure_report = _audit_structure(target_root, seen_ids, total, valid)
    findings.extend(structure_report["findings"])

    by_code: dict[str, int] = {}
    by_sev: dict[str, int] = {}
    for item in findings:
        by_code[item["code"]] = by_code.get(item["code"], 0) + 1
        by_sev[item["severity"]] = by_sev.get(item["severity"], 0) + 1

    pass_rate = round(valid / total, 4) if total else 1.0
    return {
        "validated": True,
        "target_root": target_root.as_posix(),
        "total": total,
        "valid": valid,
        "findings": findings,
        "structure": structure_report["metrics"],
        "summary": {
            "findings_total": len(findings),
            "by_severity": by_sev,
            "by_code": by_code,
            "pass_rate": pass_rate,
            "structure_conformant": structure_report["conformant"],
        },
    }


def _longest_chain(node: str, graph: dict[str, list[str]], visited: set[str]) -> int:
    if node in visited:
        return 0
    visited = visited | {node}
    deps = graph.get(node) or []
    if not deps:
        return 0
    return 1 + max(_longest_chain(dep, graph, visited) for dep in deps)


def _audit_structure(
    target_root: Path,
    seen_ids: dict[str, str],
    total: int,
    valid: int,
) -> dict[str, Any]:
    findings: list[dict[str, Any]] = []
    metrics: dict[str, Any] = {}

    graph: dict[str, list[str]] = {}
    tier_counts: dict[str, int] = {}
    for tier_dir in target_root.iterdir():
        if not tier_dir.is_dir() or tier_dir.name not in _VALID_TIERS:
            continue
        tier_counts[tier_dir.name] = 0
        for f in tier_dir.glob("*.json"):
            tier_counts[tier_dir.name] += 1
            try:
                doc = json.loads(f.read_text(encoding="utf-8"))
            except (json.JSONDecodeError, OSError):
                continue
            cid = str(doc.get("id") or "")
            deps = doc.get("made_of") or []
            if isinstance(deps, list) and cid:
                graph[cid] = [str(d) for d in deps]

    max_depth = 0
    depth_violations = 0
    for node in graph:
        depth = _longest_chain(node, graph, visited=set())
        if depth > max_depth:
            max_depth = depth
        if depth > MAX_COMPOSITION_DEPTH:
            depth_violations += 1
            findings.append({
                "severity": "error",
                "code": "CHAIN_DEPTH_EXCEEDED",
                "component": node,
                "depth": depth,
                "limit": MAX_COMPOSITION_DEPTH,
            })
    metrics["chain_depth"] = {
        "limit": MAX_COMPOSITION_DEPTH,
        "observed_max": max_depth,
        "violations": depth_violations,
        "conformant": depth_violations == 0,
    }

    metrics["tier_distribution"] = tier_counts

    dup_count = sum(1 for f in findings if f.get("code") == "DUPLICATE_ID")
    dup_fraction = dup_count / total if total else 0
    dup_ok = dup_fraction < DUPLICATE_ID_TOLERANCE
    if not dup_ok:
        findings.append({
            "severity": "warn",
            "code": "HIGH_DUPLICATE_FRACTION",
            "observed_fraction": dup_fraction,
            "tolerance": DUPLICATE_ID_TOLERANCE,
        })
    metrics["duplicate_ids"] = {
        "count": dup_count,
        "fraction": dup_fraction,
        "conformant": dup_ok,
    }

    pass_rate = round(valid / total, 4) if total else 1.0
    pass_ok = pass_rate >= QUALITY_FLOOR
    metrics["pass_rate"] = {
        "floor": QUALITY_FLOOR,
        "observed": pass_rate,
        "conformant": pass_ok,
    }

    conformant = (
        metrics["chain_depth"]["conformant"]
        and metrics["duplicate_ids"]["conformant"]
        and metrics["pass_rate"]["conformant"]
    )
    return {"findings": findings, "metrics": metrics, "conformant": conformant}


def emit_certificate(
    rebuild_receipt: dict[str, Any],
    audit: dict[str, Any],
    *,
    out_dir: Path | None = None,
) -> dict[str, Any]:
    """Write a SHA-256-bound rebuild certificate next to the rebuild folder."""
    target_root = Path(rebuild_receipt.get("target_root", "") or (out_dir or Path(".")))
    cert_path = target_root / "CERTIFICATE.json"

    body = {
        "certificate_version": "ASSADE-SPEC-CERT-1",
        "issued_at": dt.datetime.now(dt.timezone.utc).isoformat(),
        "rebuild_tag": rebuild_receipt.get("rebuild_tag"),
        "source_plan_digest": rebuild_receipt.get("source_plan_digest"),
        "target_root": rebuild_receipt.get("target_root"),
        "written_count": rebuild_receipt.get("written_count"),
        "audit": {
            "total": audit.get("total"),
            "valid": audit.get("valid"),
            "summary": audit.get("summary"),
            "structure": audit.get("structure"),
        },
        "issuer": "ass_ade.engine.schema_rebuilder",
        "schema_covered": COMPONENT_SCHEMA,
    }
    blob = json.dumps(body, sort_keys=True).encode("utf-8")
    body["certificate_sha256"] = hashlib.sha256(blob).hexdigest()
    cert_path.write_text(
        json.dumps(body, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    return {
        "certificate_path": cert_path.as_posix(),
        "certificate_sha256": body["certificate_sha256"],
        "structure_conformant": audit.get("summary", {}).get("structure_conformant", False),
    }
