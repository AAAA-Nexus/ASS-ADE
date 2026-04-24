"""Sidecar audit on synthetic materialized trees."""

from __future__ import annotations

import json
from pathlib import Path

from ass_ade.a0_qk_constants.schemas import COMPONENT_SCHEMA_V11
from ass_ade.a1_at_functions.audit_rebuild import validate_rebuild_v11


def _minimal_sidecar(component_id: str, tier_dir: str) -> dict:
    return {
        "component_schema": COMPONENT_SCHEMA_V11,
        "id": component_id,
        "tier": tier_dir,
        "name": "n",
        "kind": "pure_function",
        "description": "d",
        "made_of": [],
        "provides": [],
        "reuse_policy": "synthesize",
        "status": "draft",
    }


def test_validate_rebuild_accepts_valid_a1_sidecar(tmp_path: Path) -> None:
    tdir = tmp_path / "a1_at_functions"
    tdir.mkdir()
    sid = "a1.test.fixture.x"
    (tdir / "x.json").write_text(
        json.dumps(_minimal_sidecar(sid, "a1_at_functions"), indent=2) + "\n",
        encoding="utf-8",
    )
    r = validate_rebuild_v11(tmp_path)
    assert r["validated"] is True
    assert r["total"] == 1
    assert r["valid"] == 1
    assert r["summary"]["structure_conformant"] is True


def test_validate_rebuild_rejects_bad_prefix(tmp_path: Path) -> None:
    tdir = tmp_path / "a1_at_functions"
    tdir.mkdir()
    bad = _minimal_sidecar("a2.wrong.prefix", "a1_at_functions")
    (tdir / "bad.json").write_text(json.dumps(bad) + "\n", encoding="utf-8")
    r = validate_rebuild_v11(tmp_path)
    assert r["valid"] == 0
    assert r["summary"]["structure_conformant"] is False
