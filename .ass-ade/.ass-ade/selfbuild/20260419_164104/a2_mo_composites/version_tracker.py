"""Version Tracker — per-module semantic versioning for the rebuild engine.

Every materialized component gets a semver version. On incremental rebuilds:
  - New file: 0.1.0
  - Content unchanged: keep same version
  - API preserved, internals changed: patch bump  (0.1.3 → 0.1.4)
  - New public symbols added: minor bump           (0.1.3 → 0.2.0)
  - Public symbols removed or renamed: major bump  (0.1.3 → 1.0.0) + warning

Tier folders get a VERSION.json with aggregate version + module list.
The rebuild root gets a VERSION file with the overall build version.
"""

from __future__ import annotations

import ast
import hashlib
import json
import re
from pathlib import Path
from typing import Any

INITIAL_VERSION = "0.1.0"
_SEMVER_RE = re.compile(r"^(\d+)\.(\d+)\.(\d+)$")


# ── Semver helpers ────────────────────────────────────────────────────────────

def _parse_semver(version: str) -> tuple[int, int, int] | None:
    m = _SEMVER_RE.match(version or "")
    if not m:
        return None
    return int(m.group(1)), int(m.group(2)), int(m.group(3))


def _fmt(major: int, minor: int, patch: int) -> str:
    return f"{major}.{minor}.{patch}"


def bump_version(current: str, change_type: str) -> str:
    """Bump a semver string by 'major', 'minor', or 'patch'."""
    parsed = _parse_semver(current)
    if parsed is None:
        return INITIAL_VERSION
    major, minor, patch = parsed
    if change_type == "major":
        return _fmt(major + 1, 0, 0)
    if change_type == "minor":
        return _fmt(major, minor + 1, 0)
    return _fmt(major, minor, patch + 1)


def _aggregate_version(versions: list[str]) -> str:
    """Return the highest semver from a list."""
    best: tuple[int, int, int] = _parse_semver(INITIAL_VERSION) or (0, 1, 0)
    for v in versions:
        parsed = _parse_semver(v)
        if parsed and parsed > best:
            best = parsed
    return _fmt(*best)


# ── Content hashing ───────────────────────────────────────────────────────────

def content_hash(text: str) -> str:
    """SHA-256 (first 16 hex chars) of whitespace-normalised content."""
    normalised = "\n".join(line.rstrip() for line in text.splitlines()).strip()
    return hashlib.sha256(normalised.encode("utf-8")).hexdigest()[:16]


# ── API change detection ──────────────────────────────────────────────────────

def _public_python_api(body: str) -> set[str]:
    if not body:
        return set()
    try:
        tree = ast.parse(body)
    except SyntaxError:
        return set()
    names: set[str] = set()
    for node in ast.iter_child_nodes(tree):
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
            if not node.name.startswith("_"):
                names.add(node.name)
        elif isinstance(node, ast.Assign):
            for target in node.targets:
                if isinstance(target, ast.Name) and not target.id.startswith("_"):
                    names.add(target.id)
    return names


def _public_ts_api(body: str) -> set[str]:
    names: set[str] = set()
    for pat in (
        re.compile(r"^\s*export\s+(?:function|class|const|let|var)\s+([A-Za-z_$][\w$]*)", re.MULTILINE),
    ):
        for m in pat.finditer(body):
            names.add(m.group(1))
    return names


def classify_change(old_body: str, new_body: str, language: str = "python") -> str:
    """Classify the nature of change between two body texts.

    Returns: 'none' | 'patch' | 'minor' | 'major'
    """
    if old_body == new_body:
        return "none"
    if language == "python":
        old_api = _public_python_api(old_body)
        new_api = _public_python_api(new_body)
    elif language in {"typescript", "javascript"}:
        old_api = _public_ts_api(old_body)
        new_api = _public_ts_api(new_body)
    else:
        return "patch"

    removed = old_api - new_api
    added = new_api - old_api
    if removed:
        return "major"
    if added:
        return "minor"
    return "patch"


# ── Version assignment ────────────────────────────────────────────────────────

def assign_version(
    artifact_id: str,
    new_body: str,
    language: str,
    prev_versions: dict[str, dict[str, Any]],
) -> tuple[str, str]:
    """Return (version_string, change_type) for a component artifact.

    Args:
        artifact_id:   Component id (e.g. ``at.source.myapp.parse_token``).
        new_body:      Source body of the new/updated component (may be empty).
        language:      'python', 'typescript', 'rust', etc.
        prev_versions: Previous build's version map (from ``load_prev_versions``).

    Returns:
        (version, change_type) where change_type is one of:
        'new', 'none', 'patch', 'minor', 'major'.
    """
    prev = prev_versions.get(artifact_id)
    if prev is None:
        return INITIAL_VERSION, "new"

    new_hash = content_hash(new_body)
    if prev.get("body_hash") == new_hash:
        return prev.get("version", INITIAL_VERSION), "none"

    old_body = prev.get("body", "")
    change_type = classify_change(old_body, new_body, language)
    if change_type == "none":
        return prev.get("version", INITIAL_VERSION), "none"

    return bump_version(prev.get("version", INITIAL_VERSION), change_type), change_type


# ── Tier / project version files ──────────────────────────────────────────────

def write_tier_version_file(
    tier_dir: Path,
    tier: str,
    module_versions: list[dict[str, Any]],
) -> str:
    """Write ``VERSION.json`` inside a tier directory.

    Args:
        tier_dir:        The tier folder (e.g. ``<root>/a1_at_functions``).
        tier:            Tier name string.
        module_versions: List of ``{id, name, version, change_type}`` dicts.

    Returns:
        Absolute path of the written file.
    """
    all_versions = [m.get("version", INITIAL_VERSION) for m in module_versions]
    tier_version = _aggregate_version(all_versions)
    payload: dict[str, Any] = {
        "tier": tier,
        "tier_version": tier_version,
        "module_count": len(module_versions),
        "modules": sorted(module_versions, key=lambda m: m.get("id", "")),
    }
    path = tier_dir / "VERSION.json"
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return path.as_posix()


def write_project_version_file(
    target_root: Path,
    tier_versions: dict[str, str],
    rebuild_tag: str,
) -> str:
    """Write a plain-text ``VERSION`` file at the rebuild root.

    Format::

        0.2.1
        rebuild_tag=20260418_153000
        tiers=a0_qk_constants,a1_at_functions,...

    Returns:
        Absolute path of the written file.
    """
    project_version = _aggregate_version(list(tier_versions.values())) if tier_versions else INITIAL_VERSION
    lines = [
        project_version,
        f"rebuild_tag={rebuild_tag}",
        f"tiers={','.join(sorted(tier_versions))}",
    ]
    path = target_root / "VERSION"
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return path.as_posix()


# ── Previous build loading ────────────────────────────────────────────────────

def load_prev_versions(prev_manifest_path: Path | None) -> dict[str, dict[str, Any]]:
    """Load version data from a previous build's MANIFEST.json.

    Returns a dict keyed by component id with keys:
    ``version``, ``body_hash``, ``body``.
    """
    if prev_manifest_path is None or not prev_manifest_path.exists():
        return {}
    try:
        manifest = json.loads(prev_manifest_path.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        return {}
    result: dict[str, dict[str, Any]] = {}
    for comp in manifest.get("components") or []:
        cid = comp.get("id")
        if cid:
            result[cid] = {
                "version": comp.get("version", INITIAL_VERSION),
                "body_hash": comp.get("body_hash", ""),
                "body": comp.get("body", ""),
            }
    return result
