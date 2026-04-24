"""Tests for the FastAPI AG-UI server (a3_og_features.ag_ui_server).

These tests use FastAPI's TestClient; they are skipped if fastapi is not
installed (so pure-core installs still pass the suite).
"""

from __future__ import annotations

import json
from pathlib import Path

import pytest

fastapi = pytest.importorskip("fastapi")
from fastapi.testclient import TestClient  # noqa: E402


def _server(working_dir: Path) -> TestClient:
    from ass_ade.a2_mo_composites.ag_ui_bus import reset_bus
    from ass_ade.a3_og_features.ag_ui_server import build_app

    reset_bus()
    app = build_app(working_dir=working_dir)
    return TestClient(app)


def test_health(tmp_path: Path) -> None:
    client = _server(tmp_path)
    r = client.get("/health")
    assert r.status_code == 200
    body = r.json()
    assert body["status"] == "ok"
    assert body["working_dir"].endswith(tmp_path.name)


def test_commands_endpoint_returns_cli_palette(tmp_path: Path) -> None:
    client = _server(tmp_path)
    r = client.get("/commands")
    assert r.status_code == 200
    body = r.json()
    assert body["total"] > 10
    names = {c["name"] for c in body["commands"]}
    assert "scout" in names
    assert "ui" in names
    assert "categories" in body


def test_state_snapshot(tmp_path: Path) -> None:
    client = _server(tmp_path)
    r = client.get("/state")
    assert r.status_code == 200
    assert r.json() == {}


def test_scout_reports_empty_when_none_on_disk(tmp_path: Path) -> None:
    client = _server(tmp_path)
    r = client.get("/scout/reports")
    assert r.status_code == 200
    assert r.json() == []


def test_assimilation_summary_reads_scout_reports(tmp_path: Path) -> None:
    ass_ade = tmp_path / ".ass-ade"
    ass_ade.mkdir()
    (ass_ade / "scout-a.json").write_text(
        json.dumps({
            "schema_version": "ass-ade.scout/v1",
            "repo": "/tmp/a",
            "summary": {"total_files": 5, "total_dirs": 2},
            "symbol_summary": {"symbols": 10, "tested_symbols": 3, "python_files": 4},
            "target_map": {
                "action_counts": {"assimilate": 2, "skip": 1},
                "targets": [],
            },
            "llm": {"status": "skipped"},
            "static_recommendations": [],
        }),
        encoding="utf-8",
    )
    client = _server(tmp_path)
    r = client.get("/assimilation/summary")
    assert r.status_code == 200
    body = r.json()
    assert body["stats"]["repos_scouted"] == 1
    assert body["stats"]["action_totals"]["assimilate"] == 2


def test_memory_personality_returns_defaults(tmp_path: Path) -> None:
    client = _server(tmp_path)
    r = client.get("/memory/personality")
    assert r.status_code == 200
    body = r.json()
    assert body["persona"] in {
        "co-pilot", "mentor", "commander", "architect", "debug-buddy",
    }


def test_skills_endpoint_lists_builtin_skills(tmp_path: Path) -> None:
    client = _server(tmp_path)
    r = client.get("/skills")
    assert r.status_code == 200
    names = {s["name"] for s in r.json()}
    assert "scout" in names  # our newly integrated scout skill
    assert "git" in names
    assert "debug" in names
