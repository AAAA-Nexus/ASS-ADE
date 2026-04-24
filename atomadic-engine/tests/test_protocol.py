from pathlib import Path

from typer.testing import CliRunner

from ass_ade.cli import app
from ass_ade.config import AssAdeConfig
from ass_ade.protocol.cycle import render_protocol_markdown, run_protocol
from ass_ade.protocol.evolution import (
    bump_project_version,
    record_evolution_event,
    render_branch_evolution_demo,
)

runner = CliRunner()


def test_run_protocol_builds_report_for_repo(tmp_path: Path) -> None:
    (tmp_path / "README.md").write_text("# Demo\n", encoding="utf-8")
    (tmp_path / "docs").mkdir()
    (tmp_path / "docs" / "architecture.md").write_text("x", encoding="utf-8")
    (tmp_path / "docs" / "dev-stack.md").write_text("x", encoding="utf-8")
    (tmp_path / "docs" / "protocol.md").write_text("x", encoding="utf-8")
    (tmp_path / ".github").mkdir()
    (tmp_path / ".github" / "copilot-instructions.md").write_text("x", encoding="utf-8")
    (tmp_path / "src").mkdir()
    (tmp_path / "src" / "ass_ade").mkdir()
    (tmp_path / "src" / "ass_ade" / "cli.py").write_text("x", encoding="utf-8")
    (tmp_path / "src" / "ass_ade" / "nexus").mkdir(parents=True)
    (tmp_path / "src" / "ass_ade" / "nexus" / "models.py").write_text("x", encoding="utf-8")
    (tmp_path / "src" / "ass_ade" / "local").mkdir(parents=True)
    (tmp_path / "src" / "ass_ade" / "local" / "repo.py").write_text("x", encoding="utf-8")
    (tmp_path / "tests").mkdir()
    (tmp_path / "tests" / "test_cli.py").write_text("x", encoding="utf-8")
    (tmp_path / "pyproject.toml").write_text("[project]\nname='demo'\n", encoding="utf-8")

    report = run_protocol("Improve public shell", tmp_path, AssAdeConfig(profile="local"))

    assert report.goal == "Improve public shell"
    assert report.assessment.profile == "local"
    assert len(report.audit) == 5
    assert report.summary.startswith("Completed a public-safe enhancement cycle")


def test_render_protocol_markdown_contains_sections(tmp_path: Path) -> None:
    (tmp_path / "README.md").write_text("# Demo\n", encoding="utf-8")
    report = run_protocol("Improve public shell", tmp_path, AssAdeConfig(profile="local"))
    markdown = render_protocol_markdown(report)

    assert "# ASS-ADE Public Enhancement Cycle" in markdown
    assert "## Assessment" in markdown
    assert "## Audit" in markdown
    assert "## Recommendations" in markdown


def test_record_evolution_event_writes_ledger_and_markdown(tmp_path: Path) -> None:
    (tmp_path / "pyproject.toml").write_text(
        '[project]\nname = "demo"\nversion = "0.0.1"\n',
        encoding="utf-8",
    )

    result = record_evolution_event(
        root=tmp_path,
        event_type="birth",
        summary="First public-safe birth record",
        commands=[],
        metrics={"tests_passed": 1150},
        reports=["RECON_REPORT.md"],
        timestamp_utc="2026-04-18T12:00:00Z",
    )

    assert Path(result.ledger_path).exists()
    assert Path(result.snapshot_path).exists()
    markdown = Path(result.markdown_path).read_text(encoding="utf-8")
    assert "First public-safe birth record" in markdown
    assert "`tests_passed`: 1150" in markdown


def test_render_branch_evolution_demo_names_tracks(tmp_path: Path) -> None:
    (tmp_path / "pyproject.toml").write_text(
        '[project]\nname = "demo"\nversion = "0.0.1"\n',
        encoding="utf-8",
    )

    markdown = render_branch_evolution_demo(
        root=tmp_path,
        branches=["tests-first", "docs-first"],
        iterations=2,
    )

    assert "git switch -c evolve/tests-first" in markdown
    assert "docs-first iteration 2" in markdown
    assert "ass-ade protocol evolution-record" in markdown


def test_bump_project_version_updates_public_surfaces(tmp_path: Path) -> None:
    (tmp_path / "pyproject.toml").write_text(
        '[project]\nname = "demo"\nversion = "0.0.1"\n',
        encoding="utf-8",
    )
    package_dir = tmp_path / "src" / "ass_ade"
    package_dir.mkdir(parents=True)
    (package_dir / "__init__.py").write_text('__version__ = "0.0.1"\n', encoding="utf-8")
    (tmp_path / "README.md").write_text("# Demo\n\n**Version:** 0.0.1\n", encoding="utf-8")
    (tmp_path / "CHANGELOG.md").write_text("# Changelog\n\n## [Unreleased]\n", encoding="utf-8")

    result = bump_project_version(
        root=tmp_path,
        bump="minor",
        summary="Prepare next evolution branch",
    )

    assert result.old_version == "0.0.1"
    assert result.new_version == "0.1.0"
    assert 'version = "0.1.0"' in (tmp_path / "pyproject.toml").read_text(encoding="utf-8")
    assert '__version__ = "0.1.0"' in (package_dir / "__init__.py").read_text(encoding="utf-8")
    assert "**Version:** 0.1.0" in (tmp_path / "README.md").read_text(encoding="utf-8")
    assert "## [0.1.0]" in (tmp_path / "CHANGELOG.md").read_text(encoding="utf-8")
    assert result.backup_dir
    assert len(result.files_backed_up) == 4
    assert (Path(result.backup_dir) / "pyproject.toml").exists()


def test_bump_project_version_preserves_showcase_readme_without_version_line(tmp_path: Path) -> None:
    (tmp_path / "pyproject.toml").write_text(
        '[project]\nname = "demo"\nversion = "0.0.1"\n',
        encoding="utf-8",
    )
    package_dir = tmp_path / "src" / "ass_ade"
    package_dir.mkdir(parents=True)
    (package_dir / "__init__.py").write_text('__version__ = "0.0.1"\n', encoding="utf-8")
    readme = tmp_path / "README.md"
    showcase = b"# Showcase README\r\n\r\nNo version marker here.\r\n"
    readme.write_bytes(showcase)

    result = bump_project_version(root=tmp_path, bump="patch")

    assert readme.read_bytes() == showcase
    assert str(readme) not in result.files_updated


def test_protocol_evolution_record_cli(tmp_path: Path) -> None:
    (tmp_path / "pyproject.toml").write_text(
        '[project]\nname = "demo"\nversion = "0.0.1"\n',
        encoding="utf-8",
    )

    result = runner.invoke(
        app,
        [
            "protocol",
            "evolution-record",
            "iteration",
            "--summary",
            "CLI event",
            "--path",
            str(tmp_path),
            "--command",
            "status=passed::python -m pytest tests/ -q --no-header",
            "--metric",
            "tests=1",
        ],
    )

    assert result.exit_code == 0
    assert "Evolution Event Recorded" in result.stdout
    assert (tmp_path / ".ass-ade" / "evolution" / "ledger.jsonl").exists()
