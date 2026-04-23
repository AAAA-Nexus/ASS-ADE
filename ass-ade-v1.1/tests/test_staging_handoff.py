from __future__ import annotations

import json
import subprocess
from pathlib import Path

import pytest
from typer.testing import CliRunner

from ass_ade_v11.a4_sy_orchestration.unified_cli import app as unified_app
from ass_ade_v11.ade.staging_handoff import build_staging_handoff_summary


def _write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def _write_bytes(path: Path, data: bytes) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(data)


def _init_clean_git_repo(repo: Path) -> None:
    subprocess.run(["git", "init", "-b", "main"], cwd=repo, check=True, capture_output=True, text=True)
    subprocess.run(["git", "config", "user.email", "tests@example.invalid"], cwd=repo, check=True, capture_output=True, text=True)
    subprocess.run(["git", "config", "user.name", "ASS-ADE Tests"], cwd=repo, check=True, capture_output=True, text=True)
    subprocess.run(["git", "add", "."], cwd=repo, check=True, capture_output=True, text=True)
    subprocess.run(["git", "commit", "-m", "initial"], cwd=repo, check=True, capture_output=True, text=True)
    subprocess.run(
        ["git", "remote", "add", "origin", "https://example.invalid/AAAA-Nexus/ASS-ADE.git"],
        cwd=repo,
        check=True,
        capture_output=True,
        text=True,
    )


def _seed_ship_surface(root: Path) -> None:
    _write(
        root / "pyproject.toml",
        "\n".join(
            [
                "[project]",
                'name = "ass-ade"',
                'version = "1.0.0"',
                "",
                "[project.scripts]",
                'ass-ade = "ass_ade_v11.a4_sy_orchestration.unified_cli:main"',
                'atomadic = "ass_ade_v11.a4_sy_orchestration.unified_cli:main"',
                "",
            ]
        ),
    )
    _write(root / "README.md", "# ASS-ADE\n")
    _write(root / "docs" / "PUBLIC_SHOWCASE_README.md", "# ASS-ADE\n")
    _write(root / "LICENSE", "Proprietary\n")
    _write(root / "CONTRIBUTING.md", "# Contributing\n")
    _write(root / "SECURITY.md", "# Security Policy\n")
    _write(root / ".github" / "ISSUE_TEMPLATE" / "bug_report.yml", "name: Bug report\n")
    _write(root / ".github" / "ISSUE_TEMPLATE" / "feature_request.yml", "name: Feature request\n")
    _write(root / ".github" / "ISSUE_TEMPLATE" / "config.yml", "blank_issues_enabled: false\n")
    _write(root / ".github" / "dependabot.yml", "version: 2\n")
    _write(root / ".github" / "PULL_REQUEST_TEMPLATE.md", "## Summary\n")
    _write(root / ".github" / "workflows" / "ass-ade-ship.yml", "name: ass-ade-ship\n")


def test_build_staging_handoff_summary_ok_when_surfaces_match(tmp_path: Path) -> None:
    private_root = tmp_path / "private"
    staging_root = tmp_path / "staging"
    private_root.mkdir()
    staging_root.mkdir()
    _seed_ship_surface(private_root)
    _seed_ship_surface(staging_root)
    _init_clean_git_repo(staging_root)

    summary = build_staging_handoff_summary(
        private_root=private_root,
        staging_root=staging_root,
        required_paths=[
            "pyproject.toml",
            "README.md",
            ".github/workflows/ass-ade-ship.yml",
        ],
    )

    assert summary["ok"] is True
    assert summary["verdict"] == "READY_FOR_PUSH"
    assert summary["private_missing_required_paths"] == []
    assert summary["staging_missing_required_paths"] == []
    assert summary["content_mismatches"] == []
    assert summary["staging_git"]["is_clean"] is True
    assert summary["staging_git"]["has_remotes"] is True


def test_build_staging_handoff_summary_flags_missing_paths_and_dirty_git(tmp_path: Path) -> None:
    private_root = tmp_path / "private"
    staging_root = tmp_path / "staging"
    private_root.mkdir()
    staging_root.mkdir()
    _seed_ship_surface(private_root)
    _write(staging_root / "pyproject.toml", '[project]\nname = "ass-ade"\nversion = "0.1.0"\n')
    _write(staging_root / "README.md", "# Older ASS-ADE\n")
    _init_clean_git_repo(staging_root)
    _write(staging_root / "scratch.txt", "dirty tree\n")

    summary = build_staging_handoff_summary(
        private_root=private_root,
        staging_root=staging_root,
        required_paths=[
            "pyproject.toml",
            "README.md",
            ".github/workflows/ass-ade-ship.yml",
        ],
    )

    assert summary["ok"] is False
    assert ".github/workflows/ass-ade-ship.yml" in summary["staging_missing_required_paths"]
    assert any(row["path"] == "pyproject.toml" for row in summary["content_mismatches"])
    assert summary["staging_git"]["is_clean"] is False
    assert summary["staging_git"]["dirty_count"] >= 1
    assert "staging_git_dirty" in summary["notes"]


def test_build_staging_handoff_summary_uses_public_showcase_readme_as_source(tmp_path: Path) -> None:
    private_root = tmp_path / "private"
    staging_root = tmp_path / "staging"
    private_root.mkdir()
    staging_root.mkdir()
    _seed_ship_surface(private_root)
    _seed_ship_surface(staging_root)
    _write(private_root / "README.md", "# Private workspace readme\n")
    _write(private_root / "docs" / "PUBLIC_SHOWCASE_README.md", "# Public release readme\n")
    _write(staging_root / "README.md", "# Public release readme\n")
    _init_clean_git_repo(staging_root)

    summary = build_staging_handoff_summary(
        private_root=private_root,
        staging_root=staging_root,
        required_paths=["README.md"],
    )

    assert summary["ok"] is True
    assert summary["content_mismatches"] == []
    assert summary["source_overrides"] == {"README.md": "docs/PUBLIC_SHOWCASE_README.md"}


def test_build_staging_handoff_summary_tolerates_crlf_checkout_for_text_files(tmp_path: Path) -> None:
    private_root = tmp_path / "private"
    staging_root = tmp_path / "staging"
    private_root.mkdir()
    staging_root.mkdir()
    _seed_ship_surface(private_root)
    _seed_ship_surface(staging_root)
    _write_bytes(private_root / "CONTRIBUTING.md", b"# Contributing\nLine two\n")
    _write_bytes(staging_root / "CONTRIBUTING.md", b"# Contributing\r\nLine two\r\n")
    _init_clean_git_repo(staging_root)

    summary = build_staging_handoff_summary(
        private_root=private_root,
        staging_root=staging_root,
        required_paths=["CONTRIBUTING.md"],
    )

    assert summary["ok"] is True
    assert summary["content_mismatches"] == []


@pytest.mark.cli
def test_unified_ade_ship_audit_cli_outputs_json(tmp_path: Path) -> None:
    private_root = tmp_path / "private"
    staging_root = tmp_path / "staging"
    private_root.mkdir()
    staging_root.mkdir()
    _seed_ship_surface(private_root)
    _seed_ship_surface(staging_root)
    _init_clean_git_repo(staging_root)

    runner = CliRunner()
    result = runner.invoke(
        unified_app,
        [
            "ade",
            "ship-audit",
            "--private-root",
            str(private_root),
            "--staging-root",
            str(staging_root),
            "--no-default-paths",
            "--require-path",
            "pyproject.toml",
            "--require-path",
            "README.md",
            "--require-path",
            ".github/workflows/ass-ade-ship.yml",
        ],
    )

    assert result.exit_code == 0, result.stdout + (result.stderr or "")
    payload = json.loads(result.stdout)
    assert payload["ok"] is True
    assert payload["staging_git"]["branch"] == "main"
