"""Tier a1 — assimilated function 'run_phase4_validate'

Assimilated from: phase4_validate.py:11-30
"""

from __future__ import annotations

# --- imports from original module ---
from __future__ import annotations

from typing import Any

from ass_ade.a1_at_functions.cycle_detector import break_cycles, detect_cycles
from ass_ade.a1_at_functions.tier_purity import enforce_tier_purity


# --- assimilated symbol ---
def run_phase4_validate(
    gap_plan: dict[str, Any],
    *,
    break_cycles_if_found: bool = True,
    enforce_purity: bool = True,
) -> dict[str, Any]:
    cycle_report = detect_cycles(gap_plan)
    out: dict[str, Any] = {
        "phase": 4,
        "cycles": {
            "cycle_count": cycle_report["cycle_count"],
            "nodes_in_cycles": cycle_report["nodes_in_cycles"],
            "acyclic": cycle_report["acyclic"],
        },
    }
    if not cycle_report["acyclic"] and break_cycles_if_found:
        out["cycles"]["break_receipt"] = break_cycles(gap_plan, cycle_report)
    if enforce_purity:
        out["tier_purity"] = enforce_tier_purity(gap_plan)
    return out

