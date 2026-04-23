"""Full rebuild pipeline phases 0–7 (no Nexus synthesis / forge).

Aligned with the **ass-ade-v1*** self-rebuilt artifact layout under
``C:\\!atomadic\\ass-ade-v1`` (MANIFEST / CERTIFICATE / BLUEPRINT at repo root).
Books include ``reference_ass_ade_v1`` when ``ASS_ADE_V1_REFERENCE_ROOT`` resolves.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any, Sequence

from ass_ade_v11.a3_og_features.pipeline_book import run_book_until


def run_rebuild_v11(
    source_root: Path,
    output_parent: Path,
    *,
    extra_source_roots: Sequence[Path | str] = (),
    root_ids: list[str] | None = None,
    rebuild_tag: str | None = None,
    root_id: str | None = None,
    registry: list[dict[str, Any]] | None = None,
    blueprints: list[dict[str, Any]] | None = None,
    task_description: str = "rebuild",
    break_cycles_if_found: bool = True,
    enforce_purity: bool = True,
    distribution_name: str = "ass-ade-rebuilt-v11",
) -> dict[str, Any]:
    """Recon → ingest → gap-fill → enrich → validate → materialize → audit → package."""
    return run_book_until(
        source_root,
        Path(output_parent),
        extra_source_roots=extra_source_roots,
        root_ids=root_ids,
        stop_after=7,
        rebuild_tag=rebuild_tag,
        root_id=root_id,
        registry=registry,
        blueprints=blueprints,
        task_description=task_description,
        break_cycles_if_found=break_cycles_if_found,
        enforce_purity=enforce_purity,
        distribution_name=distribution_name,
    )
