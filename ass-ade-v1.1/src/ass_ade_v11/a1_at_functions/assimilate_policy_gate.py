"""Pure gates for multi-root ``assimilate`` policy (S2 / ASS_ADE_SHIP_PLAN Phase 2)."""

from __future__ import annotations

import json
import os
from pathlib import Path
from typing import Any


def assimilation_policy_gate_enforced() -> bool:
    """True when ``--also`` runs must carry a ``--policy`` file (CI or explicit flag)."""
    ci = os.environ.get("CI", "").strip().lower() in {"1", "true", "yes"}
    flag = os.environ.get("ASS_ADE_ASSIMILATE_REQUIRE_POLICY", "").strip().lower() in {
        "1",
        "true",
        "yes",
    }
    return ci or flag


def parse_assimilate_policy_yaml(text: str) -> Any:
    """Parse policy YAML text to a Python object (requires PyYAML when used)."""
    try:
        import yaml  # type: ignore[import-untyped]
    except ImportError as exc:  # pragma: no cover - exercised via install surface
        raise RuntimeError(
            "PyYAML is required for --policy; install with pip install -e \".[dev]\" "
            "from the repository root."
        ) from exc
    return yaml.safe_load(text)


def default_assimilate_policy_schema_path() -> Path:
    """Resolve ``assimilate-policy.schema.json`` (wheel-safe bundle under ``ass_ade_v11``)."""
    bundled = (
        Path(__file__).resolve().parents[1] / "_bundled_ade_specs" / "assimilate-policy.schema.json"
    )
    if bundled.is_file():
        return bundled
    # Editable checkout without bundled data (exotic): legacy `.ass-ade/specs/` next to spine root.
    return Path(__file__).resolve().parents[3] / ".ass-ade" / "specs" / "assimilate-policy.schema.json"


def validate_assimilate_policy_jsonschema(doc: Any, *, schema_path: Path) -> None:
    """Validate document against the checked-in JSON Schema (draft 2020-12)."""
    try:
        from jsonschema import Draft202012Validator  # type: ignore[import-untyped]
        from jsonschema.exceptions import ValidationError  # type: ignore[import-untyped]
    except ImportError as exc:  # pragma: no cover
        raise RuntimeError(
            "jsonschema is required for JSON Schema validation; "
            'install with pip install -e ".[dev]" from the repository root.'
        ) from exc
    schema = json.loads(schema_path.read_text(encoding="utf-8"))
    try:
        Draft202012Validator(schema).validate(doc)
    except ValidationError as exc:
        raise ValueError(f"assimilate policy failed JSON Schema: {exc.message}") from exc


def validate_assimilate_policy_document(doc: Any) -> None:
    """Structural check aligned with ``.ass-ade/specs/assimilate-policy.schema.json`` (minimal)."""
    if not isinstance(doc, dict):
        raise ValueError("assimilate policy root must be a mapping")
    if doc.get("schema_version") != "1":
        raise ValueError("assimilate policy schema_version must be '1'")
    primary = doc.get("primary")
    if not isinstance(primary, dict):
        raise ValueError("assimilate policy 'primary' must be a mapping")
    if primary.get("role") != "map":
        raise ValueError("assimilate policy primary.role must be 'map'")
    if not isinstance(primary.get("path"), str) or not primary["path"].strip():
        raise ValueError("assimilate policy primary.path must be a non-empty string")
    roots = doc.get("roots")
    if not isinstance(roots, list) or len(roots) < 1:
        raise ValueError("assimilate policy 'roots' must be a non-empty array")
    allowed_roles = {"map", "sibling", "input", "archive", "ephemeral"}
    allowed_license = {
        "compatible_oss",
        "copyleft_review",
        "proprietary",
        "unknown",
    }
    for i, row in enumerate(roots):
        if not isinstance(row, dict):
            raise ValueError(f"assimilate policy roots[{i}] must be a mapping")
        for key in ("path", "role", "license_class"):
            if key not in row:
                raise ValueError(f"assimilate policy roots[{i}] missing '{key}'")
        if row["role"] not in allowed_roles:
            raise ValueError(f"assimilate policy roots[{i}].role invalid")
        if row["license_class"] not in allowed_license:
            raise ValueError(f"assimilate policy roots[{i}].license_class invalid")


def load_and_validate_assimilate_policy(
    path: Path,
    *,
    schema_path: Path | None = None,
    skip_jsonschema: bool = False,
) -> dict[str, Any]:
    """Load YAML from disk, structurally validate, then JSON Schema when available."""
    text = path.read_text(encoding="utf-8")
    doc = parse_assimilate_policy_yaml(text)
    validate_assimilate_policy_document(doc)
    if not isinstance(doc, dict):
        raise ValueError("internal: policy document must be dict after validation")
    sp = schema_path or default_assimilate_policy_schema_path()
    if not skip_jsonschema and sp.is_file():
        validate_assimilate_policy_jsonschema(doc, schema_path=sp)
    return doc
