"""Build and validate ``ASSIMILATE_PLAN`` JSON (B1/B2) from a book result."""

from __future__ import annotations

import datetime as dt
import json
from pathlib import Path
from typing import Any


def default_assimilate_plan_schema_path() -> Path:
    """Resolve ``assimilate-plan.schema.json`` (wheel-safe bundle under ``ass_ade``)."""
    bundled = (
        Path(__file__).resolve().parents[1] / "_bundled_ade_specs" / "assimilate-plan.schema.json"
    )
    if bundled.is_file():
        return bundled
    return Path(__file__).resolve().parents[3] / ".ass-ade" / "specs" / "assimilate-plan.schema.json"


def validate_assimilate_plan_jsonschema(doc: Any, *, schema_path: Path) -> None:
    """Validate plan document against the checked-in JSON Schema (draft 2020-12)."""
    try:
        from jsonschema import Draft202012Validator  # type: ignore[import-untyped]
        from jsonschema.exceptions import ValidationError  # type: ignore[import-untyped]
    except ImportError as exc:  # pragma: no cover
        raise RuntimeError(
            "jsonschema is required for ASSIMILATE_PLAN validation; "
            'install with pip install -e ".[dev]" from the repository root.'
        ) from exc
    schema = json.loads(schema_path.read_text(encoding="utf-8"))
    try:
        Draft202012Validator(schema).validate(doc)
    except ValidationError as exc:
        raise ValueError(f"ASSIMILATE_PLAN failed JSON Schema: {exc.message}") from exc


def build_assimilate_plan_document(
    *,
    book: dict[str, Any],
    primary: Path,
    output_parent: Path | None,
    extra_roots: list[Path],
    stop_after_label: str,
    policy: dict[str, Any] | None,
) -> dict[str, Any]:
    """Minimal B1/B2 plan object aligned with ``assimilate-plan.schema.json``."""
    p0 = book.get("phase0") or {}
    verdict = p0.get("verdict")
    p1 = book.get("phase1") or {}
    raw_ns = p1.get("namespace_conflicts")
    conflicts_list: list[dict[str, Any]] = []
    if isinstance(raw_ns, dict):
        for c in raw_ns.get("conflicts") or []:
            if isinstance(c, dict) and "stem" in c:
                conflicts_list.append(
                    {
                        "qualified_name": str(c["stem"]),
                        "source_roots": [str(x) for x in (c.get("sources") or [])],
                        "resolution_recommendation": str(c.get("resolution") or "primary_wins"),
                    }
                )

    actions: list[str] = []
    if verdict != "READY_FOR_PHASE_1":
        actions.append("Review phase0 recon; fix exclusions or terrain until READY_FOR_PHASE_1.")
    if conflicts_list:
        actions.append("Resolve namespace conflicts; primary MAP wins on duplicate symbols by default.")
    if policy is None and len(extra_roots) > 0:
        actions.append("Consider authoring assimilate-policy.yaml for long-lived multi-root runs.")

    now = dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

    doc: dict[str, Any] = {
        "schema_version": "1",
        "generated_at_utc": now,
        "primary_path": primary.resolve().as_posix(),
        "extra_roots": [p.resolve().as_posix() for p in extra_roots],
        "book_stop_after": stop_after_label.strip().lower(),
        "phase0_status": str(verdict or ""),
        "ready_for_phase_1": verdict == "READY_FOR_PHASE_1",
        "namespace_conflicts": conflicts_list,
        "recommended_human_actions": actions,
    }
    if output_parent is not None:
        doc["output_parent"] = output_parent.resolve().as_posix()
    if policy is not None:
        doc["assimilate_policy_schema_version"] = policy.get("schema_version")

    p2 = book.get("phase2") or {}
    if isinstance(p2, dict) and p2:
        stubs = p2.get("stub_components") or p2.get("stubs") or []
        if isinstance(stubs, list):
            doc["gapfill_summary"] = {"stub_count": len(stubs), "tier_gaps": []}

    return doc


def build_validate_assimilate_plan(
    *,
    book: dict[str, Any],
    primary: Path,
    output_parent: Path | None,
    extra_roots: list[Path],
    stop_after_label: str,
    policy: dict[str, Any] | None,
    schema_path: Path | None = None,
    skip_jsonschema: bool = False,
) -> dict[str, Any]:
    """Build plan object and validate when schema file is present."""
    doc = build_assimilate_plan_document(
        book=book,
        primary=primary,
        output_parent=output_parent,
        extra_roots=extra_roots,
        stop_after_label=stop_after_label,
        policy=policy,
    )
    sp = schema_path or default_assimilate_plan_schema_path()
    if not skip_jsonschema and sp.is_file():
        validate_assimilate_plan_jsonschema(doc, schema_path=sp)
    return doc
