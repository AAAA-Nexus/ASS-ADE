"""Tier a2 — assimilated class 'TaskResult'

Assimilated from: rebuild/forge.py:241-251
"""

from __future__ import annotations


# --- assimilated symbol ---
class TaskResult:
    """Result of executing one ForgeTask."""

    task_id: str
    file: str
    node: str
    issue: str
    fixed_code: str | None
    verified: bool
    error: str | None = None
    diff_summary: str = ""

