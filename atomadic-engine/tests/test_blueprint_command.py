"""Smoke tests for the ``ass-ade blueprint`` sub-command."""

from __future__ import annotations

import json
from pathlib import Path

import typer
from typer.testing import CliRunner

from ass_ade.commands.blueprint import blueprint_app, register_blueprint_app


runner = CliRunner()


def _write_blueprint(tmp_path: Path, name: str = "blueprint_smoke.json") -> Path:
    path = tmp_path / name
    payload = {
        "schema": "AAAA-SPEC-004",
        "description": "smoke test blueprint",
        "components": [
            {"id": "at_smoke", "tier": "a1_at_functions"},
        ],
        "tiers": ["a0_qk_constants", "a1_at_functions"],
    }
    path.write_text(json.dumps(payload), encoding="utf-8")
    return path


def test_blueprint_list_empty_directory(tmp_path: Path) -> None:
    result = runner.invoke(blueprint_app, ["list", "--dir", str(tmp_path)])
    assert result.exit_code == 0
    assert "no blueprints" in result.stdout.lower()


def test_blueprint_list_finds_blueprints(tmp_path: Path) -> None:
    _write_blueprint(tmp_path)
    result = runner.invoke(blueprint_app, ["list", "--dir", str(tmp_path)])
    assert result.exit_code == 0
    assert "blueprint_smoke.json" in result.stdout


def test_blueprint_validate_ok(tmp_path: Path) -> None:
    bp = _write_blueprint(tmp_path)
    result = runner.invoke(blueprint_app, ["validate", str(bp)])
    assert result.exit_code == 0
    assert "valid" in result.stdout.lower()


def test_blueprint_validate_rejects_missing_schema(tmp_path: Path) -> None:
    bp = tmp_path / "bad.json"
    bp.write_text(json.dumps({"description": "no schema"}), encoding="utf-8")
    result = runner.invoke(blueprint_app, ["validate", str(bp)])
    assert result.exit_code == 1
    assert "schema" in result.stdout.lower()


def test_blueprint_validate_rejects_bad_json(tmp_path: Path) -> None:
    bp = tmp_path / "broken.json"
    bp.write_text("{not-json", encoding="utf-8")
    result = runner.invoke(blueprint_app, ["validate", str(bp)])
    assert result.exit_code != 0


def test_register_blueprint_app_mounts_subcommand() -> None:
    parent = typer.Typer()
    register_blueprint_app(parent)
    result = runner.invoke(parent, ["blueprint", "--help"])
    assert result.exit_code == 0
    assert "blueprint" in result.stdout.lower()
