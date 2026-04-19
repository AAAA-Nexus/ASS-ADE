# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a0_qk_constants/qk_draft_validate_rebuild.py:7
# Component id: qk.source.a0_qk_constants.validate_rebuild
from __future__ import annotations

__version__ = "0.1.0"

def validate_rebuild(target_root: Path) -> dict[str, Any]:
    """Lint every materialized component JSON under ``target_root``.

    Checks:
      1. All required top-level fields present
      2. tier is one of the five known values
      3. id prefix matches tier
      4. File lives in the correct tier subdirectory
      5. ``component_schema`` equals ASSADE-SPEC-003
      6. ``made_of`` is a list
      7. No duplicate ids

    Returns a compact report the orchestrator folds into the rebuild receipt.
    """
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
