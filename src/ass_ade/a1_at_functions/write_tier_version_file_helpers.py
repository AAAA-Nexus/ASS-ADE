"""Tier a1 — assimilated function 'write_tier_version_file'

Assimilated from: rebuild/version_tracker.py:165-190
"""

from __future__ import annotations


# --- assimilated symbol ---
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

