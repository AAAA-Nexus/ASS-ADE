"""Tier a1 — assimilated function 'observations_to_epiphanies'

Assimilated from: rebuild/epiphany_cycle.py:55-81
"""

from __future__ import annotations


# --- assimilated symbol ---
def observations_to_epiphanies(observations: list[str]) -> list[dict[str, object]]:
    out: list[dict[str, object]] = []
    for i, raw in enumerate(observations[:8]):
        text = str(raw).strip()
        if not text:
            continue
        out.append(
            {
                "id": f"e{i + 1}",
                "insight": text,
                "evidence_refs": [],
                "deficit_tags": [],
            }
        )
    if not out:
        out.append(
            {
                "id": "e1",
                "insight": (
                    "No observations yet — run phase0_recon (or paste failing output) "
                    "then re-run epiphany_breakthrough_cycle with observations[]."
                ),
                "evidence_refs": [],
                "deficit_tags": ["needs_grounding"],
            }
        )
    return out

