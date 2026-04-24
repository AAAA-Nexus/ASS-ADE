"""Tier a1 — assimilated function 'bump_version'

Assimilated from: rebuild/version_tracker.py:40-50
"""

from __future__ import annotations


# --- assimilated symbol ---
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

