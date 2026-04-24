"""Tier a1 — assimilated function 'run_book_until'

Assimilated from: pipeline_book.py:64-118
"""

from __future__ import annotations

# --- imports from original module ---
from __future__ import annotations

import datetime as dt
import os
from pathlib import Path
from typing import Any, Sequence

from ass_ade.a1_at_functions.conflict_detector import (


# --- assimilated symbol ---
def run_book_until(
    source_root: Path,
    output_parent: Path | None,
    *,
    stop_after: int = 7,
    rebuild_tag: str | None = None,
    root_id: str | None = None,
    root_ids: list[str] | None = None,
    extra_source_roots: list[Path] | None = None,
    registry: list[dict[str, Any]] | None = None,
    blueprints: list[dict[str, Any]] | None = None,
    task_description: str = "rebuild",
    max_body_chars: int | None = None,
    break_cycles_if_found: bool = True,
    enforce_purity: bool = True,
    distribution_name: str = "ass-ade-rebuilt-v11",
    policy_doc: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Run pipeline phases 0..``stop_after`` (inclusive). ``stop_after`` in 0..7.

    Phases 5–7 require ``output_parent`` (materialization root). Earlier phases do not.
    Each book includes ``reference_ass_ade_v1`` (MAP=TERRAIN probe for ``ass-ade-v1*``).

    Phase 0 recon runs on **every** source root (primary plus ``extra_source_roots``): each
    must be a directory with at least one ``.py`` file (after exclusions).

    When ``extra_source_roots`` is set, the first root (``source_root``) is the **primary**
    MAP terrain; additional roots merge into one gap plan. Identical Python files dedupe by
    content hash; divergent same-path modules are reported (hints) and halt the book only
    when ``namespace_merge.enforce_distinct_modules: true`` or ``ASS_ADE_ENFORCE_NAMESPACE_CNA=1``
    (``ASS_ADE_RELAX_NAMESPACE_CNA=1`` overrides enforcement off).

    When ``policy_doc`` is a validated assimilate policy, its ``roots[]`` rows are resolved
    into per-root ingest rules (``forbid_globs`` / ``allow_globs`` / ``max_file_bytes``) and
    applied to phase 1. Unmatched roots keep default (legacy) behavior.
    """
    return attach_v1_reference_index(
        _run_book_until_core(
            source_root,
            output_parent,
            stop_after=stop_after,
            rebuild_tag=rebuild_tag,
            root_id=root_id,
            root_ids=root_ids,
            extra_source_roots=extra_source_roots,
            registry=registry,
            blueprints=blueprints,
            task_description=task_description,
            max_body_chars=max_body_chars,
            break_cycles_if_found=break_cycles_if_found,
            enforce_purity=enforce_purity,
            distribution_name=distribution_name,
            policy_doc=policy_doc,
        )
    )

