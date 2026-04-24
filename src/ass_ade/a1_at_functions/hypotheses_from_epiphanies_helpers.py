"""Tier a1 — assimilated function 'hypotheses_from_epiphanies'

Assimilated from: rebuild/epiphany_cycle.py:84-95
"""

from __future__ import annotations


# --- assimilated symbol ---
def hypotheses_from_epiphanies(epiphanies: list[dict[str, object]]) -> list[dict[str, object]]:
    hy: list[dict[str, object]] = []
    for i, ep in enumerate(epiphanies[:8]):
        eid = str(ep.get("id", f"e{i + 1}"))
        hy.append(
            {
                "id": f"h{i + 1}",
                "statement": f"Address root cause suggested by {eid} with smallest reversible change.",
                "parent_epiphany_ids": [eid],
            }
        )
    return hy

