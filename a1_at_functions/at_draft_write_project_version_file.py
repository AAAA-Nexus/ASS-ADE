# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a1_at_functions/at_draft_write_project_version_file.py:7
# Component id: at.source.a1_at_functions.write_project_version_file
from __future__ import annotations

__version__ = "0.1.0"

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
