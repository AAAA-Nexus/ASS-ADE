"""Tier a1 — assimilated function 'build_stem_map'

Assimilated from: rebuild/import_rewriter.py:49-77
"""

from __future__ import annotations


# --- assimilated symbol ---
def build_stem_map(written_modules: dict[str, str]) -> dict[str, str]:
    """Build {bare_stem → qualified_name} from materialize_plan's written_modules.

    Example:
        written_modules = {
            "/old/proj/utils.py":  "/out/20260420/a1_at_functions/utils.py",
            "/old/proj/config.py": "/out/20260420/a0_qk_constants/config.py",
        }
        →  {"utils": "a1_at_functions.utils", "config": "a0_qk_constants.config"}
    """
    stem_map: dict[str, str] = {}
    for src, dest in written_modules.items():
        dest_path = Path(dest)
        tier = _extract_tier(dest_path)
        if tier:
            dest_stem = dest_path.stem
            src_stem = Path(src).stem
            # Don't map __init__ or test files
            if dest_stem.startswith("__") or dest_stem.startswith("test_"):
                continue
            qualified = f"{tier}.{dest_stem}"
            # Map both the canonical (dest) stem AND the original source stem
            # to the qualified path. Existing source imports reference the
            # original stem; tier-internal references may use the canonical.
            # First occurrence wins (sorted iteration is stable).
            stem_map.setdefault(dest_stem, qualified)
            if src_stem != dest_stem and not src_stem.startswith("__"):
                stem_map.setdefault(src_stem, qualified)
    return stem_map

