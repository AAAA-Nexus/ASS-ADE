"""Tier a2 — assimilated class 'ForgeResult'

Assimilated from: rebuild/forge.py:266-274
"""

from __future__ import annotations


# --- assimilated symbol ---
class ForgeResult:
    """Aggregate result of the full forge phase."""

    plan_tasks: int = 0
    applied: int = 0
    skipped: int = 0
    files_modified: set[str] = field(default_factory=set)
    results: list[TaskResult] = field(default_factory=list)
    model_used: str = ""

