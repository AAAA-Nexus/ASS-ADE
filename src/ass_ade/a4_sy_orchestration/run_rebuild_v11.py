"""Public entry: full v1.1 rebuild (phases 0–7)."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from ass_ade.a3_og_features.pipeline_rebuild_v11 import run_rebuild_v11


def rebuild_project_v11(
    source_root: Path | str,
    output_parent: Path | str,
    **kwargs: Any,
) -> dict[str, Any]:
    """MAP = TERRAIN orchestrator aligned with ass-ade-v1 phase order (minus forge/synthesis)."""
    return run_rebuild_v11(Path(source_root), Path(output_parent), **kwargs)
