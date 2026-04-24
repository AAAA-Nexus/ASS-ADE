"""Phase 7 — final installable layout from materialized terrain (MAP = TERRAIN)."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from ass_ade.a1_at_functions.package_layout import emit_robust_package


def run_phase7_package(
    target_root: Path,
    *,
    distribution_name: str = "ass-ade-rebuilt",
    version: str = "0.0.0",
    gap_plan: dict[str, Any] | None = None,
    output_package_name: str | None = None,
    package_root: Path | None = None,
    source_project_root: Path | None = None,
) -> dict[str, Any]:
    pkg = emit_robust_package(
        Path(target_root),
        distribution_name=distribution_name,
        version=version,
        gap_plan=gap_plan,
        output_package_name=output_package_name,
        package_root=package_root,
        source_project_root=source_project_root,
    )
    return {"phase": 7, "package": pkg}
