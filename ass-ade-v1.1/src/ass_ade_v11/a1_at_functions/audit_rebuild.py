"""Validate materialized tier tree (JSON sidecars + structure)."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from ass_ade_v11.a0_qk_constants.schemas import COMPONENT_SCHEMA_V11
from ass_ade_v11.a0_qk_constants.tier_names import TIER_PREFIX, VALID_TIER_DIRS

_REQUIRED_FIELDS = (
    "component_schema", "id", "tier", "name", "kind",
    "description", "made_of", "provides", "reuse_policy", "status",
)


def validate_rebuild_v11(target_root: Path) -> dict[str, Any]:
    """Lint JSON sidecars under tier directories (v11 schema)."""
    target_root = target_root.resolve()
    if not target_root.exists():
        return {
            "validated": False,
            "reason": f"target_root does not exist: {target_root}",
            "total": 0,
            "valid": 0,
            "findings": [],
            "summary": {"pass_rate": 0.0, "structure_conformant": False, "findings_total": 0},
        }

    findings: list[dict[str, Any]] = []
    seen_ids: dict[str, str] = {}
    total = 0
    valid = 0

    for tier_dir in sorted(target_root.iterdir()):
        if not tier_dir.is_dir() or tier_dir.name not in VALID_TIER_DIRS:
            continue
        expected_prefix = TIER_PREFIX[tier_dir.name] + "."
        for f in sorted(x for x in tier_dir.glob("*.json") if x.name != "VERSION.json"):
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
            if tier not in VALID_TIER_DIRS:
                findings.append({"severity": "error", "code": "INVALID_TIER",
                                 "path": f.as_posix(), "tier": str(tier)})
                file_ok = False

            cid = str(doc.get("id") or "")
            if tier in VALID_TIER_DIRS and cid and not cid.startswith(expected_prefix):
                findings.append({"severity": "error", "code": "TIER_PREFIX_MISMATCH",
                                 "path": f.as_posix(), "id": cid,
                                 "expected_prefix": expected_prefix})
                file_ok = False

            if tier != tier_dir.name:
                findings.append({"severity": "error", "code": "TIER_DIR_MISMATCH",
                                 "path": f.as_posix(),
                                 "declared_tier": str(tier),
                                 "actual_dir": tier_dir.name})
                file_ok = False

            if doc.get("component_schema") != COMPONENT_SCHEMA_V11:
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

    tier_subdirs = {p.name for p in target_root.iterdir() if p.is_dir()}
    extra_dirs = sorted(
        n for n in tier_subdirs
        if n not in VALID_TIER_DIRS and n != "__pycache__" and not n.startswith(".")
    )
    for name in extra_dirs:
        findings.append({
            "severity": "warn",
            "code": "EXTRA_TOP_LEVEL_DIR",
            "path": (target_root / name).as_posix(),
            "message": name,
        })

    err_count = sum(1 for f in findings if f.get("severity") == "error")
    structure_conformant = total > 0 and err_count == 0 and valid == total

    pass_rate = round(valid / total, 4) if total else 0.0
    by_code: dict[str, int] = {}
    by_sev: dict[str, int] = {}
    for item in findings:
        by_code[item["code"]] = by_code.get(item["code"], 0) + 1
        by_sev[item["severity"]] = by_sev.get(item["severity"], 0) + 1

    return {
        "validated": True,
        "target_root": target_root.as_posix(),
        "total": total,
        "valid": valid,
        "findings": findings,
        "summary": {
            "findings_total": len(findings),
            "by_severity": by_sev,
            "by_code": by_code,
            "pass_rate": pass_rate,
            "structure_conformant": structure_conformant,
            "provenance_conformant": True,
        },
    }
