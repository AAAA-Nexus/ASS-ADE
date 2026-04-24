"""Tier a1 — assimilated function 'run_phase5_materialize'

Assimilated from: phase5_materialize.py:15-44
"""

from __future__ import annotations

# --- imports from original module ---
from __future__ import annotations

from pathlib import Path
from typing import Any

from ass_ade.a1_at_functions.materialize_tiers import (


# --- assimilated symbol ---
def run_phase5_materialize(
    gap_plan: dict[str, Any],
    output_parent: Path,
    rebuild_tag: str,
    *,
    write_json_sidecars: bool = True,
    assimilation_meta: dict[str, Any] | None = None,
    source_roots: list[Path] | None = None,
    rewrite_imports: bool = True,
) -> dict[str, Any]:
    output_parent = Path(output_parent).resolve()
    plan_summary = emit_plan_blueprint_v11(gap_plan, output_parent, rebuild_tag)
    receipt = materialize_gap_plan_to_tree(
        gap_plan,
        output_parent,
        rebuild_tag,
        write_json_sidecars=write_json_sidecars,
        source_roots=source_roots,
        rewrite_imports=rewrite_imports,
    )
    assim_out: dict[str, Any] | None = None
    if assimilation_meta is not None:
        assim_out = emit_assimilation_log_v11(assimilation_meta, output_parent, rebuild_tag)
    return {
        "phase": 5,
        "plan_blueprint": plan_summary,
        "materialize": receipt,
        "target_root": receipt["target_root"],
        "assimilation": assim_out,
    }

