"""Tier a1 — assimilated function 'write_project_version_file'

Assimilated from: rebuild/version_tracker.py:193-217
"""

from __future__ import annotations


# --- assimilated symbol ---
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

