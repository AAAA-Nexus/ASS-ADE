"""Tier a2 — assimilated class 'EpiphanyPlan'

Assimilated from: rebuild/forge.py:255-262
"""

from __future__ import annotations


# --- assimilated symbol ---
class EpiphanyPlan:
    """Structured plan produced by the Epiphany analysis pass."""

    schema: str = "atomadic.epiphany-plan.v1"
    idea: str = "Improve materialized codebase"
    experiments: list[ForgeTask] = field(default_factory=list)
    vetted_sources: list[str] = field(default_factory=list)
    promoted: bool = False

