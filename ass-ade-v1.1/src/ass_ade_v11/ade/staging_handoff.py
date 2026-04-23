"""Audit the private ``!atomadic`` -> public ``!aaaa-nexus`` ASS-ADE handoff."""

from __future__ import annotations

import hashlib
import os
import subprocess
from collections.abc import Mapping
from pathlib import Path
from typing import Any, Sequence

try:
    import tomllib
except ImportError:  # pragma: no cover
    tomllib = None  # type: ignore[assignment]

from ass_ade_v11.ade.discover import find_monorepo_root

DEFAULT_REQUIRED_SHIP_PATHS: tuple[str, ...] = (
    "pyproject.toml",
    "LICENSE",
    "README.md",
    "CONTRIBUTING.md",
    "SECURITY.md",
    "ASS_ADE_SHIP_PLAN.md",
    "docs/ASS_ADE_UNIFICATION.md",
    ".github/ISSUE_TEMPLATE/bug_report.yml",
    ".github/ISSUE_TEMPLATE/feature_request.yml",
    ".github/ISSUE_TEMPLATE/config.yml",
    ".github/dependabot.yml",
    ".github/PULL_REQUEST_TEMPLATE.md",
    ".github/workflows/ass-ade-ship.yml",
    "ass-ade-v1.1/src/ass_ade_v11/a4_sy_orchestration/unified_cli.py",
)

DEFAULT_REQUIRED_SHIP_SOURCE_OVERRIDES: dict[str, str] = {
    "README.md": "docs/PUBLIC_SHOWCASE_README.md",
}


def _path_from_rel(rel_path: str) -> Path:
    return Path(*rel_path.split("/"))


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _read_project_metadata(root: Path) -> dict[str, Any] | None:
    if tomllib is None:
        return None
    pyproject = root / "pyproject.toml"
    if not pyproject.is_file():
        return None
    try:
        data = tomllib.loads(pyproject.read_text(encoding="utf-8"))
    except (OSError, UnicodeDecodeError, tomllib.TOMLDecodeError):
        return None
    project = data.get("project")
    if not isinstance(project, dict):
        return None
    scripts = project.get("scripts")
    return {
        "name": project.get("name"),
        "version": project.get("version"),
        "scripts": sorted(scripts.keys()) if isinstance(scripts, dict) else [],
    }


def _source_rel_path(
    rel_path: str,
    source_overrides: Mapping[str, str] | None,
) -> str:
    if source_overrides is None:
        return rel_path
    return source_overrides.get(rel_path, rel_path)


def _run_git(repo: Path, *args: str) -> subprocess.CompletedProcess[str] | None:
    try:
        return subprocess.run(
            ["git", "-C", str(repo), *args],
            capture_output=True,
            text=True,
            timeout=30,
            check=False,
        )
    except (OSError, subprocess.SubprocessError):
        return None


def _git_summary(repo: Path) -> dict[str, Any]:
    git_dir = repo / ".git"
    summary: dict[str, Any] = {
        "present": git_dir.is_dir(),
        "branch": "",
        "is_clean": False,
        "dirty_count": 0,
        "dirty_entries": [],
        "has_remotes": False,
        "remotes": [],
    }
    if not git_dir.is_dir():
        return summary

    branch = _run_git(repo, "branch", "--show-current")
    if branch is not None and branch.returncode == 0:
        summary["branch"] = branch.stdout.strip()

    status = _run_git(repo, "status", "--short", "--untracked-files=all")
    dirty_entries: list[str] = []
    if status is not None and status.returncode == 0:
        dirty_entries = [line for line in status.stdout.splitlines() if line.strip()]
    summary["dirty_entries"] = dirty_entries[:20]
    summary["dirty_count"] = len(dirty_entries)
    summary["is_clean"] = len(dirty_entries) == 0

    remotes_proc = _run_git(repo, "remote", "-v")
    remotes: list[dict[str, str]] = []
    if remotes_proc is not None and remotes_proc.returncode == 0:
        for line in remotes_proc.stdout.splitlines():
            parts = line.split()
            if len(parts) >= 3:
                remotes.append(
                    {
                        "name": parts[0],
                        "url": parts[1],
                        "kind": parts[2].strip("()"),
                    }
                )
    summary["remotes"] = remotes
    summary["has_remotes"] = len(remotes) > 0
    return summary


def _normalize_staging_root(candidate: Path) -> Path:
    resolved = candidate.resolve()
    if (resolved / ".git").is_dir() or (resolved / "pyproject.toml").is_file():
        return resolved
    nested = resolved / "!ass-ade"
    if (nested / ".git").is_dir() or (nested / "pyproject.toml").is_file():
        return nested
    return resolved


def discover_default_staging_root(private_root: Path) -> Path | None:
    for key in ("ATOMADIC_NEXUS_SHIP_ROOT", "ATOMADIC_NEXUS_WORKSPACE"):
        raw = (os.environ.get(key) or "").strip()
        if raw:
            return _normalize_staging_root(Path(raw))
    sibling = private_root.parent / "!aaaa-nexus" / "!ass-ade"
    if sibling.exists():
        return sibling.resolve()
    parent = private_root.parent / "!aaaa-nexus"
    if parent.exists():
        return _normalize_staging_root(parent)
    return None


def build_staging_handoff_summary(
    *,
    private_root: Path | None = None,
    staging_root: Path | None = None,
    required_paths: Sequence[str] = DEFAULT_REQUIRED_SHIP_PATHS,
    source_overrides: Mapping[str, str] | None = DEFAULT_REQUIRED_SHIP_SOURCE_OVERRIDES,
) -> dict[str, Any]:
    private = find_monorepo_root(private_root)
    if private is None:
        private = (private_root or Path.cwd()).resolve()
    staging = _normalize_staging_root(staging_root) if staging_root is not None else discover_default_staging_root(private)

    required = list(dict.fromkeys(required_paths))
    private_missing: list[str] = []
    staging_missing: list[str] = []
    content_mismatches: list[dict[str, str]] = []

    for rel_path in required:
        private_source_rel = _source_rel_path(rel_path, source_overrides)
        private_file = private / _path_from_rel(private_source_rel)
        if not private_file.is_file():
            private_missing.append(rel_path)
            continue
        if staging is None:
            staging_missing.append(rel_path)
            continue
        rel = _path_from_rel(rel_path)
        staging_file = staging / rel
        if not staging_file.is_file():
            staging_missing.append(rel_path)
            continue
        if _sha256(private_file) != _sha256(staging_file):
            content_mismatches.append(
                {
                    "path": rel_path,
                    "private_source_path": private_source_rel,
                    "private_sha256": _sha256(private_file),
                    "staging_sha256": _sha256(staging_file),
                }
            )

    git_summary = _git_summary(staging) if staging is not None and staging.exists() else _git_summary(Path("__missing__"))
    notes: list[str] = []
    if staging is None:
        notes.append("staging_root_missing")
    elif not staging.exists():
        notes.append("staging_root_missing")
    if private_missing:
        notes.append("private_surface_incomplete")
    if staging_missing:
        notes.append("staging_surface_incomplete")
    if content_mismatches:
        notes.append("staging_surface_drift")
    if not git_summary["present"]:
        notes.append("staging_git_missing")
    elif not git_summary["is_clean"]:
        notes.append("staging_git_dirty")
    if git_summary["present"] and not git_summary["has_remotes"]:
        notes.append("staging_git_remote_missing")

    ok = (
        staging is not None
        and staging.exists()
        and not private_missing
        and not staging_missing
        and not content_mismatches
        and bool(git_summary["present"])
        and bool(git_summary["is_clean"])
        and bool(git_summary["has_remotes"])
    )

    return {
        "ok": ok,
        "verdict": "READY_FOR_PUSH" if ok else "BLOCKED",
        "private_root": str(private),
        "staging_root": str(staging) if staging is not None else None,
        "required_paths": required,
        "source_overrides": dict(source_overrides or {}),
        "private_project": _read_project_metadata(private),
        "staging_project": _read_project_metadata(staging) if staging is not None and staging.exists() else None,
        "private_missing_required_paths": private_missing,
        "staging_missing_required_paths": staging_missing,
        "content_mismatches": content_mismatches,
        "staging_git": git_summary,
        "notes": notes,
    }
