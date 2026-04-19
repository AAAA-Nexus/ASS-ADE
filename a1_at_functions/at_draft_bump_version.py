# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a1_at_functions/at_draft_bump_version.py:7
# Component id: at.source.a1_at_functions.bump_version
from __future__ import annotations

__version__ = "0.1.0"

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
