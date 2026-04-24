"""Tier a2 — assimilated class 'IncompleteFunction'

Assimilated from: rebuild/finish.py:31-39
"""

from __future__ import annotations


# --- assimilated symbol ---
class IncompleteFunction:
    path: Path
    qualname: str
    lineno: int
    end_lineno: int
    col_offset: int
    signature: str
    docstring: str | None
    reason: str  # "pass" | "ellipsis" | "not_implemented" | "todo_only" | "return_none_only"

