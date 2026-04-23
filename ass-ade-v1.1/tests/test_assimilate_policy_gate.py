from __future__ import annotations

import json
from pathlib import Path

import pytest

from ass_ade_v11.a1_at_functions.assimilate_policy_gate import (
    assimilation_policy_gate_enforced,
    default_assimilate_policy_schema_path,
    load_and_validate_assimilate_policy,
    validate_assimilate_policy_document,
)


def test_assimilation_policy_gate_enforced_respects_ci(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.delenv("CI", raising=False)
    monkeypatch.delenv("ASS_ADE_ASSIMILATE_REQUIRE_POLICY", raising=False)
    assert assimilation_policy_gate_enforced() is False
    monkeypatch.setenv("CI", "true")
    assert assimilation_policy_gate_enforced() is True


def test_validate_assimilate_policy_document_minimal_ok() -> None:
    doc = {
        "schema_version": "1",
        "primary": {"role": "map", "path": "/tmp/map"},
        "roots": [
            {"path": "/tmp/map", "role": "map", "license_class": "compatible_oss"},
            {"path": "/tmp/s", "role": "sibling", "license_class": "unknown"},
        ],
    }
    validate_assimilate_policy_document(doc)


def test_validate_assimilate_policy_document_rejects_bad_version() -> None:
    with pytest.raises(ValueError, match="schema_version"):
        validate_assimilate_policy_document({"schema_version": "2", "primary": {}, "roots": []})


def test_json_schema_rejects_unknown_top_level_key(tmp_path: Path) -> None:
    sp = default_assimilate_policy_schema_path()
    if not sp.is_file():
        pytest.skip("spine schema not present at expected path")
    doc = {
        "schema_version": "1",
        "primary": {"role": "map", "path": "/x"},
        "roots": [{"path": "/x", "role": "map", "license_class": "compatible_oss"}],
        "not_in_schema": True,
    }
    p = tmp_path / "p.yaml"
    p.write_text(json.dumps(doc), encoding="utf-8")
    with pytest.raises(ValueError, match="JSON Schema"):
        load_and_validate_assimilate_policy(p, schema_path=sp)


def test_bundled_json_schemas_match_dot_ass_ade_specs() -> None:
    """Keep wheel bundle and `.ass-ade/specs` mirrors byte-identical (code-review ship note)."""
    here = Path(__file__).resolve()
    spine = here.parents[1]
    dot = spine / ".ass-ade" / "specs"
    bundled_dir = spine / "src" / "ass_ade_v11" / "_bundled_ade_specs"
    for name in ("assimilate-policy.schema.json", "assimilate-plan.schema.json"):
        a = bundled_dir / name
        b = dot / name
        assert a.is_file(), a
        assert b.is_file(), b
        assert a.read_bytes() == b.read_bytes(), name
