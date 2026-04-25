"""Tests for awareness-based wakeup and launch readiness commands."""

from __future__ import annotations

from pathlib import Path

from typer.testing import CliRunner

from ass_ade.a2_mo_composites import ambient_awareness
from ass_ade.a2_mo_composites.ambient_awareness import AmbientAwareness
from ass_ade.a2_mo_composites.launch_readiness import build_launch_readiness
from ass_ade.cli import app

runner = CliRunner()


def _seed_wake_template(root: Path) -> None:
    assets = root / "assets"
    assets.mkdir()
    (assets / "wake.html").write_text(
        "<script>\n"
        "// BEGIN_STATUS_INJECTION\n"
        "const STATUS = {};\n"
        "// END_STATUS_INJECTION\n"
        "</script>\n",
        encoding="utf-8",
    )


def test_wakeup_decision_uses_awareness_not_schedule(tmp_path: Path, monkeypatch) -> None:
    _seed_wake_template(tmp_path)
    monkeypatch.setattr(
        ambient_awareness,
        "get_system_time",
        lambda: {"hour": 8, "iso": "2026-04-24T08:00:00", "day_of_week": "Friday"},
    )
    monkeypatch.setattr(
        ambient_awareness,
        "get_user_activity_status",
        lambda _threshold: {"is_active": True, "idle_minutes": 0.2},
    )

    awareness = AmbientAwareness(tmp_path)
    decision = awareness.should_greet()

    assert decision.should_greet is True
    assert "Morning window" in decision.reason

    awareness.record_greet()
    second = awareness.should_greet()
    assert second.should_greet is False
    assert "Already greeted" in second.reason


def test_wakeup_render_injects_status(tmp_path: Path, monkeypatch) -> None:
    _seed_wake_template(tmp_path)
    monkeypatch.setattr(
        AmbientAwareness,
        "get_time_context",
        lambda self: {"hour": 8, "iso": "2026-04-24T08:00:00", "day_of_week": "Friday"},
    )
    monkeypatch.setattr(
        AmbientAwareness,
        "get_overnight_summary",
        lambda self: {
            "git_commits": [],
            "test_summary": {"total": 2, "passed": 2, "failed": 0},
            "overnight_actions": ["Ready."],
        },
    )

    rendered = AmbientAwareness(tmp_path).render_wake_page()

    text = rendered.read_text(encoding="utf-8")
    assert '"greeting_name": "Thomas & Jessica"' in text
    assert '"total": 2' in text


def test_wakeup_cli_check_json(tmp_path: Path) -> None:
    result = runner.invoke(app, ["wakeup", "--check", "--json", "--path", str(tmp_path)])

    assert result.exit_code == 0
    assert '"should_greet"' in result.stdout
    assert "scheduled" not in result.stdout.lower()


def test_launch_readiness_reports_missing_storefront_without_faking(tmp_path: Path) -> None:
    (tmp_path / "README.md").write_text("# demo\n", encoding="utf-8")
    (tmp_path / "docs").mkdir()
    (tmp_path / "docs" / "USER_MANUAL.md").write_text("# manual\n", encoding="utf-8")
    (tmp_path / "docs" / "RAG_PUBLIC_PRIVATE.md").write_text("# rag\n", encoding="utf-8")
    (tmp_path / "agents").mkdir()
    (tmp_path / "agents" / "atomadic_interpreter.md").write_text("plain\n", encoding="utf-8")

    report = build_launch_readiness(tmp_path, storefront=None)

    names = {check.name: check for check in report.checks}
    assert names["storefront_repo"].verdict == "REFINE"
    assert names["axiom_0_seed"].verdict == "REFINE"


def test_launch_cli_help() -> None:
    result = runner.invoke(app, ["launch", "--help"])

    assert result.exit_code == 0
    assert "status" in result.stdout

