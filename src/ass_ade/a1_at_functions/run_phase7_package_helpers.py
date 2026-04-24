"""Tier a1 — assimilated function 'run_phase7_package'

Assimilated from: phase7_package.py:11-24
"""

from __future__ import annotations

# --- imports from original module ---
from __future__ import annotations

from pathlib import Path
from typing import Any

from ass_ade.a1_at_functions.package_layout import emit_robust_package


# --- assimilated symbol ---
def run_phase7_package(
    target_root: Path,
    *,
    distribution_name: str = "ass-ade-rebuilt-v11",
    version: str = "0.0.0",
    gap_plan: dict[str, Any] | None = None,
) -> dict[str, Any]:
    pkg = emit_robust_package(
        Path(target_root),
        distribution_name=distribution_name,
        version=version,
        gap_plan=gap_plan,
    )
    return {"phase": 7, "package": pkg}

