"""Tier a1 — assimilated function 'route_matches'

Assimilated from: protocol.py:169-182
"""

from __future__ import annotations


# --- assimilated symbol ---
def route_matches(routes: tuple[str, ...] | list[str], agent_id: str) -> bool:
    """Return True iff ``agent_id`` is addressed by ``routes``.

    Wildcards: ``*`` and ``all`` each match any agent. Matching is exact and
    case-sensitive; there is no glob matching to keep routing deterministic.
    """
    if not routes:
        return True
    for r in routes:
        if r in ("*", "all"):
            return True
        if r == agent_id:
            return True
    return False

