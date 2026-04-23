"""Orchestration: phases 0–2 then a0-only materialization (mini-rebuild)."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from ass_ade_v11.a3_og_features.phase_a0_materialize import run_phase_a0_materialize
from ass_ade_v11.a3_og_features.pipeline_phases_0_2 import run_phases_0_through_2


def run_book_phases_0_2_a0(
    source_root: Path | str,
    material_out: Path | str,
    *,
    rebuild_tag_a0: str | None = None,
    enrich: bool = False,
    **kwargs: Any,
) -> dict[str, Any]:
    """Run recon → ingest → gap-fill, then materialize a0 stubs into ``material_out``.

    Defaults to ``enrich=False`` so the gate matches the phase-0–2 book (gap-fill only).
    Pass ``enrich=True`` to run phase-3 enrich first; materialization still reads
    ``phase2["gap_plan"]`` (mutated in place when enrich runs).
    """
    root = Path(source_root)
    out = Path(material_out)
    book = run_phases_0_through_2(root, enrich=enrich, **kwargs)
    if book.get("stopped_after", -1) < 2:
        return {**book, "a0_materialize": None}
    gap_plan = book["phase2"]["gap_plan"]
    mat = run_phase_a0_materialize(out, gap_plan, rebuild_tag=rebuild_tag_a0)
    return {**book, "a0_materialize": mat}
