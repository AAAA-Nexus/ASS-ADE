# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a1_at_functions/at_draft_calculate_next_version.py:7
# Component id: at.source.a1_at_functions.calculate_next_version
from __future__ import annotations

__version__ = "0.1.0"

def calculate_next_version(root: Path, bump: str, new_version: str = "") -> tuple[str, str]:
    old_version = read_project_version(root)
    requested = new_version.strip()
    if requested:
        if not _SEMVER_RE.match(requested):
            raise ValueError(f"Version must be semantic version-like: {requested}")
        return old_version, requested
    if bump not in {"patch", "minor", "major"}:
        raise ValueError("Bump must be one of: patch, minor, major")
    return old_version, bump_version(old_version, bump)
