import json
from pathlib import Path

import pytest
from typer.testing import CliRunner

from ass_ade.cli import app
from ass_ade.config import AssAdeConfig, write_default_config

runner = CliRunner()


def test_doctor_stays_local_by_default(tmp_path: Path) -> None:
    config_path = tmp_path / ".ass-ade" / "config.json"
    write_default_config(config_path, config=AssAdeConfig(profile="local"), overwrite=True)

    result = runner.invoke(app, ["doctor", "--config", str(config_path)])

    assert result.exit_code == 0
    assert "Remote Probe" in result.stdout
    assert "disabled" in result.stdout


def test_doctor_local_keeps_probe_disabled_when_env_has_nexus_key(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.setenv("AAAA_NEXUS_API_KEY", "aaaa-nexus-test-key-for-doctor")
    config_path = tmp_path / ".ass-ade" / "config.json"
    write_default_config(config_path, config=AssAdeConfig(profile="local"), overwrite=True)

    result = runner.invoke(app, ["doctor", "--config", str(config_path)])

    assert result.exit_code == 0
    assert "Remote Probe" in result.stdout
    assert "disabled" in result.stdout


def test_doctor_hybrid_probes_without_api_key(tmp_path: Path) -> None:
    config_path = tmp_path / ".ass-ade" / "config.json"
    write_default_config(config_path, config=AssAdeConfig(profile="hybrid"), overwrite=True)

    result = runner.invoke(app, ["doctor", "--config", str(config_path)])

    assert result.exit_code == 0
    assert "Remote Probe" in result.stdout
    assert "enabled" in result.stdout


def test_doctor_local_explicit_remote_enables_probe(tmp_path: Path) -> None:
    config_path = tmp_path / ".ass-ade" / "config.json"
    write_default_config(config_path, config=AssAdeConfig(profile="local"), overwrite=True)

    result = runner.invoke(app, ["doctor", "--config", str(config_path), "--remote"])

    assert result.exit_code == 0
    assert "Remote Probe" in result.stdout
    assert "enabled" in result.stdout


def test_nexus_commands_require_remote_opt_in_for_local_profile(tmp_path: Path) -> None:
    config_path = tmp_path / ".ass-ade" / "config.json"
    write_default_config(config_path, config=AssAdeConfig(profile="local"), overwrite=True)

    result = runner.invoke(app, ["nexus", "overview", "--config", str(config_path)])

    assert result.exit_code == 2
    assert "disabled in the local profile" in result.stdout


def test_repo_summary_command_reports_files(tmp_path: Path) -> None:
    (tmp_path / "README.md").write_text("hello", encoding="utf-8")
    (tmp_path / "src").mkdir()
    (tmp_path / "src" / "app.py").write_text("pass", encoding="utf-8")

    result = runner.invoke(app, ["repo", "summary", str(tmp_path)])

    assert result.exit_code == 0
    assert "Repo Summary" in result.stdout
    assert "Top File Types" in result.stdout


def test_protocol_run_command_reports_cycle(tmp_path: Path) -> None:
    (tmp_path / "README.md").write_text("hello", encoding="utf-8")

    result = runner.invoke(app, ["protocol", "run", "Improve the public shell", "--path", str(tmp_path)])

    assert result.exit_code == 0
    assert "ASS-ADE Protocol Report" in result.stdout
    assert "Audit" in result.stdout


def test_full_cycle_command_runs_locally(tmp_path: Path) -> None:
    (tmp_path / "README.md").write_text("hello", encoding="utf-8")

    result = runner.invoke(app, ["cycle", "Enhance via cycle", "--path", str(tmp_path)])

    assert result.exit_code == 0
    assert "ASS-ADE Full Cycle" in result.stdout
    assert "Protocol Summary" in result.stdout


def test_full_cycle_command_writes_report(tmp_path: Path) -> None:
    (tmp_path / "README.md").write_text("hello", encoding="utf-8")
    report_path = tmp_path / "reports" / "cycle.md"

    result = runner.invoke(
        app,
        [
            "cycle",
            "Enhance via cycle",
            "--path",
            str(tmp_path),
            "--report-out",
            str(report_path),
        ],
    )

    assert result.exit_code == 0
    assert report_path.exists()
    assert "ASS-ADE Public Enhancement Cycle" in report_path.read_text(encoding="utf-8")


def test_full_cycle_command_writes_json_report(tmp_path: Path) -> None:
    (tmp_path / "README.md").write_text("hello", encoding="utf-8")
    json_report_path = tmp_path / "reports" / "cycle.json"

    result = runner.invoke(
        app,
        [
            "cycle",
            "Enhance via cycle",
            "--path",
            str(tmp_path),
            "--json-out",
            str(json_report_path),
        ],
    )

    assert result.exit_code == 0
    assert json_report_path.exists()
    payload = json.loads(json_report_path.read_text(encoding="utf-8"))
    assert payload["goal"] == "Enhance via cycle"
    assert "report" in payload


# ── New UX feature tests ───────────────────────────────────────────────────────


def test_doctor_json_flag(tmp_path: Path) -> None:
    config_path = tmp_path / ".ass-ade" / "config.json"
    write_default_config(config_path, config=AssAdeConfig(profile="local"), overwrite=True)

    result = runner.invoke(app, ["doctor", "--config", str(config_path), "--json"])

    assert result.exit_code == 0
    payload = json.loads(result.stdout)
    assert "profile" in payload
    assert "tools" in payload
    assert payload["profile"] == "local"


def test_rebuild_dry_run(tmp_path: Path) -> None:
    src = tmp_path / "myproject"
    src.mkdir()
    (src / "main.py").write_text("def hello(): pass\n", encoding="utf-8")
    out = tmp_path / "myproject-rebuilt"

    result = runner.invoke(app, ["rebuild", str(src), str(out), "--dry-run"])

    assert result.exit_code == 0
    assert "Dry-run preview" in result.stdout
    assert not out.exists(), "--dry-run must not create output folder"


def test_rebuild_dry_run_json(tmp_path: Path) -> None:
    src = tmp_path / "myproject"
    src.mkdir()
    (src / "main.py").write_text("X = 1\n", encoding="utf-8")
    out = tmp_path / "myproject-rebuilt"

    result = runner.invoke(app, ["rebuild", str(src), str(out), "--dry-run", "--json"])

    assert result.exit_code == 0
    payload = json.loads(result.stdout)
    assert payload["dry_run"] is True
    assert "by_tier" in payload
    assert not out.exists()


def test_rebuild_yes_skips_confirmation(tmp_path: Path) -> None:
    src = tmp_path / "proj"
    src.mkdir()
    (src / "util.py").write_text("def add(a, b): return a + b\n", encoding="utf-8")
    out = tmp_path / "proj-out"

    result = runner.invoke(app, ["rebuild", str(src), str(out), "--yes", "--no-certify"])

    assert result.exit_code == 0
    assert out.exists()


def test_rebuild_json_output(tmp_path: Path) -> None:
    src = tmp_path / "proj"
    src.mkdir()
    (src / "util.py").write_text("def add(a, b): return a + b\n", encoding="utf-8")
    out = tmp_path / "proj-out"

    result = runner.invoke(app, ["rebuild", str(src), str(out), "--yes", "--no-certify", "--json"])

    assert result.exit_code == 0
    payload = json.loads(result.stdout)
    assert payload.get("ok") is True
    assert "components_written" in payload
    assert "by_tier" in payload


def test_rebuild_backs_up_existing_output(tmp_path: Path) -> None:
    src = tmp_path / "proj"
    src.mkdir()
    (src / "util.py").write_text("def add(a, b): return a + b\n", encoding="utf-8")
    out = tmp_path / "proj-out"
    out.mkdir()
    (out / "old.txt").write_text("old output\n", encoding="utf-8")

    result = runner.invoke(app, ["rebuild", str(src), str(out), "--yes", "--no-certify", "--json"])

    assert result.exit_code == 0
    payload = json.loads(result.stdout)
    backup_path = Path(payload["output_backup"])
    assert backup_path.exists()
    assert (backup_path / "old.txt").read_text(encoding="utf-8") == "old output\n"


def test_rebuild_preserves_existing_showcase_readme(tmp_path: Path) -> None:
    src = tmp_path / "proj"
    src.mkdir()
    (src / "util.py").write_text("def add(a, b): return a + b\n", encoding="utf-8")
    out = tmp_path / "proj-out"
    out.mkdir()
    showcase = b"# Showcase README\r\n\r\nKeep the hand-authored public page.\r\n"
    (out / "README.md").write_bytes(showcase)

    result = runner.invoke(app, ["rebuild", str(src), str(out), "--yes", "--no-certify", "--json"])

    assert result.exit_code == 0
    assert (out / "README.md").read_bytes() == showcase
    generated = (out / "0_README.md").read_text(encoding="utf-8")
    assert "Auto-generated by ASS-ADE rebuild engine" in generated


def test_rebuild_copies_local_env_without_tracking_hint(tmp_path: Path) -> None:
    src = tmp_path / "proj"
    src.mkdir()
    (src / "util.py").write_text("def add(a, b): return a + b\n", encoding="utf-8")
    (src / ".env").write_text("AAAA_NEXUS_API_KEY=local-secret\n", encoding="utf-8")
    out = tmp_path / "proj-out"

    result = runner.invoke(app, ["rebuild", str(src), str(out), "--yes", "--no-certify", "--json"])

    assert result.exit_code == 0
    payload = json.loads(result.stdout)
    assert payload["env_handoff"] == str(out / ".env")
    assert (out / ".env").read_text(encoding="utf-8") == "AAAA_NEXUS_API_KEY=local-secret\n"
    assert ".env" in (out / ".gitignore").read_text(encoding="utf-8")


def test_rebuild_incremental_no_manifest(tmp_path: Path) -> None:
    src = tmp_path / "proj"
    src.mkdir()
    (src / "util.py").write_text("def foo(): pass\n", encoding="utf-8")
    out = tmp_path / "proj-out"

    result = runner.invoke(
        app, ["rebuild", str(src), str(out), "--yes", "--no-certify", "--incremental"]
    )

    assert result.exit_code == 0


def test_rollback_no_backup(tmp_path: Path) -> None:
    target = tmp_path / "myproject"
    target.mkdir()
    (target / "main.py").write_text("pass\n", encoding="utf-8")

    result = runner.invoke(app, ["rollback", str(target), "--yes"])

    assert result.exit_code == 1
    assert "No backup" in result.stdout


def test_rollback_restores_backup(tmp_path: Path) -> None:
    target = tmp_path / "myproject"
    target.mkdir()
    (target / "main.py").write_text("v2\n", encoding="utf-8")

    backup = tmp_path / "myproject-backup-20240101-120000"
    backup.mkdir()
    (backup / "main.py").write_text("v1\n", encoding="utf-8")

    result = runner.invoke(app, ["rollback", str(target), "--yes"])

    assert result.exit_code == 0
    assert (target / "main.py").read_text(encoding="utf-8") == "v1\n"


def test_rollback_json(tmp_path: Path) -> None:
    target = tmp_path / "myproject"
    target.mkdir()
    (target / "main.py").write_text("v2\n", encoding="utf-8")

    backup = tmp_path / "myproject-backup-20240101-120000"
    backup.mkdir()
    (backup / "main.py").write_text("v1\n", encoding="utf-8")

    result = runner.invoke(app, ["rollback", str(target), "--yes", "--json"])

    assert result.exit_code == 0
    payload = json.loads(result.stdout)
    assert payload["ok"] is True
    assert "backup_name" in payload


def test_auto_detect_helper(tmp_path: Path) -> None:
    (tmp_path / "app.py").write_text("x = 1\n", encoding="utf-8")
    (tmp_path / "util.py").write_text("def f(): pass\n", encoding="utf-8")

    from ass_ade.cli import _auto_detect_project
    result = _auto_detect_project(tmp_path)

    assert "Python" in result
    assert "files" in result
    assert "Try:" in result

