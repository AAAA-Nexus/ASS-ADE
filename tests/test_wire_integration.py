"""Integration tests for the wire command + skill + server endpoints.

Verifies the Context Loader Wiring Specialist is exposed through every layer:
CLI (commands/wire.py), skill (SkillRunner), REPL meta-command (@wire),
and FastAPI dashboard (/wire/scan, /wire/apply, /assimilation/manifest).
"""

from __future__ import annotations

import json
from pathlib import Path

import pytest
from typer.testing import CliRunner

from ass_ade.cli import app


def _make_violating_tree(root: Path) -> Path:
    """Create a tiny monadic source tree with one upward import violation."""
    pkg = root / "src" / "demo_pkg"
    pkg.mkdir(parents=True)
    (pkg / "__init__.py").write_text("", encoding="utf-8")
    (pkg / "a0_qk_constants").mkdir()
    (pkg / "a0_qk_constants" / "__init__.py").write_text("", encoding="utf-8")
    (pkg / "a1_at_functions").mkdir()
    (pkg / "a1_at_functions" / "__init__.py").write_text("", encoding="utf-8")
    (pkg / "a3_og_features").mkdir()
    (pkg / "a3_og_features" / "__init__.py").write_text("", encoding="utf-8")

    # a3 has a real symbol
    (pkg / "a3_og_features" / "feature.py").write_text(
        "def helper(x):\n    return x * 2\n", encoding="utf-8"
    )
    # a1 ALSO defines helper (so the specialist can propose a fix)
    (pkg / "a1_at_functions" / "helpers.py").write_text(
        "def helper(x):\n    return x * 2\n", encoding="utf-8"
    )
    # a1 file with an UPWARD import from a3 — this is the violation
    (pkg / "a1_at_functions" / "bad_import.py").write_text(
        "from demo_pkg.a3_og_features.feature import helper\n\n"
        "def use_helper(x):\n    return helper(x)\n",
        encoding="utf-8",
    )
    # Minimal pyproject so package detection works
    (root / "pyproject.toml").write_text(
        '[project]\nname = "demo_pkg"\nversion = "0.1"\n', encoding="utf-8"
    )
    return pkg


def test_cli_wire_dry_run_reports_violations_without_writing(tmp_path: Path) -> None:
    _make_violating_tree(tmp_path)
    bad = tmp_path / "src" / "demo_pkg" / "a1_at_functions" / "bad_import.py"
    before = bad.read_text(encoding="utf-8")

    runner = CliRunner()
    result = runner.invoke(app, ["wire", str(tmp_path / "src" / "demo_pkg"), "--json"])
    assert result.exit_code == 0, result.stdout
    # File must be unchanged — dry-run must not write
    assert bad.read_text(encoding="utf-8") == before

    payload = json.loads(result.stdout)
    assert payload["dry_run"] is True
    assert payload["violations_found"] >= 1
    assert payload["auto_fixed"] == 0


def test_cli_wire_apply_actually_patches_file(tmp_path: Path) -> None:
    _make_violating_tree(tmp_path)
    bad = tmp_path / "src" / "demo_pkg" / "a1_at_functions" / "bad_import.py"
    before = bad.read_text(encoding="utf-8")

    runner = CliRunner()
    result = runner.invoke(
        app, ["wire", str(tmp_path / "src" / "demo_pkg"), "--apply", "--json"]
    )
    assert result.exit_code == 0, result.stdout
    after = bad.read_text(encoding="utf-8")
    assert after != before, "wire --apply should have rewritten the bad import"
    assert "a3_og_features" not in after, "upward import should be gone"


def test_wire_skill_matches_on_natural_language(tmp_path: Path) -> None:
    from ass_ade.a3_og_features.skill_runner import SkillRunner

    _make_violating_tree(tmp_path)
    runner = SkillRunner(tmp_path)
    matched = runner.match("wire imports for this tier")
    assert matched is not None
    assert matched.name == "wire"


def test_wire_skill_dry_run_output(tmp_path: Path) -> None:
    from ass_ade.a3_og_features.skill_runner import SkillContext, SkillRunner

    _make_violating_tree(tmp_path)
    runner = SkillRunner(tmp_path)
    skill = runner.get("wire")
    assert skill is not None
    ctx = SkillContext(
        user_input="wire imports",
        working_dir=tmp_path,
        tone="casual",
        domain_level="intermediate",
    )
    out = runner.run(skill, ctx)
    assert "Wire scan" in out
    assert "dry-run" in out.lower()


def test_at_wire_handler_returns_dry_run_summary(tmp_path: Path) -> None:
    from ass_ade.interpreter import Atomadic, _handle_at_command

    _make_violating_tree(tmp_path)
    agent = Atomadic(working_dir=tmp_path)
    out = _handle_at_command(agent, "wire", "")
    assert "Wire scan" in out


# ── Server endpoints ──────────────────────────────────────────────────────

fastapi = pytest.importorskip("fastapi")
from fastapi.testclient import TestClient  # noqa: E402


def _server(working_dir: Path) -> TestClient:
    from ass_ade.a2_mo_composites.ag_ui_bus import reset_bus
    from ass_ade.a3_og_features.ag_ui_server import build_app

    reset_bus()
    return TestClient(build_app(working_dir=working_dir))


def test_server_wire_scan_dry_run(tmp_path: Path) -> None:
    _make_violating_tree(tmp_path)
    client = _server(tmp_path)
    r = client.post("/wire/scan", json={})
    assert r.status_code == 200
    body = r.json()
    assert body["dry_run"] is True
    assert body["violations_found"] >= 1
    assert body["verdict"] in {"PASS", "REFINE", "DRY_RUN"}


def test_server_wire_apply_writes_patches(tmp_path: Path) -> None:
    _make_violating_tree(tmp_path)
    bad = tmp_path / "src" / "demo_pkg" / "a1_at_functions" / "bad_import.py"
    before = bad.read_text(encoding="utf-8")

    client = _server(tmp_path)
    r = client.post("/wire/apply", json={})
    assert r.status_code == 200
    body = r.json()
    assert body.get("dry_run") is not True or body.get("files_changed", 0) > 0
    assert bad.read_text(encoding="utf-8") != before


def test_server_assimilation_manifest_not_present(tmp_path: Path) -> None:
    client = _server(tmp_path)
    r = client.get("/assimilation/manifest")
    assert r.status_code == 200
    assert r.json() == {"present": False}


def test_server_assimilation_manifest_reads_cherry_pick_json(tmp_path: Path) -> None:
    ass_ade = tmp_path / ".ass-ade"
    ass_ade.mkdir()
    manifest = {
        "schema_version": "ass-ade.cherry-pick/v1",
        "source_label": "/tmp/src",
        "target_root": str(tmp_path),
        "selected_count": 3,
        "items": [
            {"action": "assimilate", "qualname": "a"},
            {"action": "assimilate", "qualname": "b"},
            {"action": "skip", "qualname": "c"},
        ],
    }
    (ass_ade / "cherry_pick.json").write_text(json.dumps(manifest), encoding="utf-8")

    client = _server(tmp_path)
    r = client.get("/assimilation/manifest")
    assert r.status_code == 200
    body = r.json()
    assert body["present"] is True
    assert body["selected_count"] == 3
    assert body["_action_totals"] == {"assimilate": 2, "skip": 1}


def test_widget_kind_wiring_report_registered() -> None:
    from ass_ade.a0_qk_constants.widget_cards import WIDGET_CARD_SCHEMAS, WiringReportCard

    assert "wiring_report" in WIDGET_CARD_SCHEMAS
    assert WIDGET_CARD_SCHEMAS["wiring_report"] is WiringReportCard
