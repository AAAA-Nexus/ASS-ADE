"""Tests for Epiphany → Breakthrough pure cycle helpers."""

from __future__ import annotations

import json

from ass_ade.engine.rebuild import epiphany_cycle as ec
from ass_ade.local.planner import draft_epiphany_breakthrough_plan, resolve_plan_track


def test_detect_track_integration() -> None:
    track, steps = ec.detect_track_and_steps("Add nexus MCP client adapter")
    assert track == "integration"
    assert any("OpenAPI" in s for s in steps)


def test_build_document_validates() -> None:
    doc = ec.build_epiphany_document(
        "Harden MCP trust path",
        track="integration",
        plan_steps=["a", "b"],
        recon_verdict="OK",
        recon_files=["src/x.py"],
        observations=["401 on stale token"],
    )
    assert ec.validate_epiphany_document(doc) == []
    assert doc["schema_version"] == ec.SCHEMA_VERSION
    assert doc["epiphanies"][0]["insight"] == "401 on stale token"


def test_draft_epiphany_breakthrough_plan_includes_phases() -> None:
    steps = draft_epiphany_breakthrough_plan("verify qa harness", max_steps=20)
    assert ec.EPIPHANY_PHASE_STEPS[0] in steps
    assert "--- Track-specific steps ---" in steps


def test_resolve_plan_track_alias() -> None:
    assert resolve_plan_track("docs only")[0] == "documentation"


def test_json_roundtrip_stable_keys() -> None:
    doc = ec.build_epiphany_document(
        "goal",
        track="implementation",
        plan_steps=["p1"],
        recon_verdict=None,
        recon_files=[],
        observations=[],
    )
    text = json.dumps(doc)
    again = json.loads(text)
    assert again["schema_version"] == ec.SCHEMA_VERSION
