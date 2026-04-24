"""Tier a1 — pure helpers for the update/channel subsystem."""

from __future__ import annotations

import re
import urllib.request
from typing import NamedTuple

_PYPI_URL = "https://pypi.org/pypi/{package}/json"
_VERSION_RE = re.compile(r"^(\d+)\.(\d+)\.(\d+)(?:\.?(dev|a|b|rc)(\d+))?$")


class VersionInfo(NamedTuple):
    major: int
    minor: int
    patch: int
    pre: str   # "" for stable, "dev"/"a"/"b"/"rc"
    pre_n: int


def parse_version(v: str) -> VersionInfo | None:
    m = _VERSION_RE.match(v.lstrip("v"))
    if not m:
        return None
    return VersionInfo(int(m.group(1)), int(m.group(2)), int(m.group(3)), m.group(4) or "", int(m.group(5) or 0))


def version_gt(a: str, b: str) -> bool:
    """Return True if a > b (a is newer)."""
    av, bv = parse_version(a), parse_version(b)
    if av is None or bv is None:
        return False
    # stable > prerelease of same base
    if av[:3] == bv[:3]:
        if av.pre == "" and bv.pre != "":
            return True
        if av.pre != "" and bv.pre == "":
            return False
        return av[4] > bv[4]
    return av[:3] > bv[:3]


def fetch_latest_version(package: str, channel: str = "stable", timeout: int = 5) -> str | None:
    """Fetch the latest version from PyPI for a given channel."""
    try:
        url = _PYPI_URL.format(package=package)
        with urllib.request.urlopen(url, timeout=timeout) as resp:
            import json
            data = json.loads(resp.read())
        releases: dict[str, list] = data.get("releases", {})
        candidates = []
        for version_str, files in releases.items():
            if not files:
                continue
            vi = parse_version(version_str)
            if vi is None:
                continue
            if channel == "stable" and vi.pre:
                continue
            if channel == "beta" and vi.pre not in ("", "b", "rc"):
                continue
            candidates.append(version_str)
        if not candidates:
            return None
        # sort by parsed version descending
        candidates.sort(key=lambda v: parse_version(v) or VersionInfo(0, 0, 0, "", 0), reverse=True)
        return candidates[0]
    except Exception:
        return None


def format_update_status(current: str, latest: str | None, channel: str) -> str:
    if latest is None:
        return f"Current: {current}  (could not reach PyPI)"
    if version_gt(latest, current):
        return f"Update available!  {current} → {latest}  (channel: {channel})"
    return f"Up to date: {current}  (channel: {channel})"
