"""Public orchestration entry for the phase 0–3 book."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from ass_ade_v11.a3_og_features.pipeline_phases_0_2 import (
    run_phases_0_through_2,
    run_phases_0_through_3,
)


def run_book_phases_0_2(source_root: Path | str, **kwargs: Any) -> dict[str, Any]:
    """Run through phase 3 by default (enrich=True); pass enrich=False to stop at gap-fill."""
    root = Path(source_root)
    return run_phases_0_through_2(root, **kwargs)


def run_book_phases_0_3(source_root: Path | str, **kwargs: Any) -> dict[str, Any]:
    """Explicit phase-3 book entry."""
    root = Path(source_root)
    return run_phases_0_through_3(root, **kwargs)
