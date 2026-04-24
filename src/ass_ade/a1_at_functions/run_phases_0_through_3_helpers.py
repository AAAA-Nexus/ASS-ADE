"""Tier a1 — assimilated function 'run_phases_0_through_3'

Assimilated from: pipeline_phases_0_2.py:63-68
"""

from __future__ import annotations

# --- imports from original module ---
from __future__ import annotations

from pathlib import Path
from typing import Any, Sequence

from ass_ade.a1_at_functions.v1_reference_index import attach_v1_reference_index
from ass_ade.a3_og_features.phase0_recon_multi import run_phase0_recon_multi
from ass_ade.a3_og_features.phase1_ingest import run_phase1_ingest_multi
from ass_ade.a3_og_features.phase2_gapfill import run_phase2_gapfill
from ass_ade.a3_og_features.phase3_enrich import run_phase3_enrich
from ass_ade.a3_og_features.pipeline_book import unique_source_roots


# --- assimilated symbol ---
def run_phases_0_through_3(
    source_root: Path,
    **kwargs: Any,
) -> dict[str, Any]:
    """Alias with explicit phase-3 naming (enrich=True)."""
    return run_phases_0_through_2(source_root, enrich=True, **kwargs)

