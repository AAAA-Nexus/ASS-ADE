# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a1_at_functions/at_draft_write_tier_version_file.py:7
# Component id: at.source.a1_at_functions.write_tier_version_file
from __future__ import annotations

__version__ = "0.1.0"

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
