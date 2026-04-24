"""Tier a1 — assimilated function 'run_rebuild_v11'

Assimilated from: pipeline_rebuild_v11.py:16-46
"""

from __future__ import annotations


# --- assimilated symbol ---
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

