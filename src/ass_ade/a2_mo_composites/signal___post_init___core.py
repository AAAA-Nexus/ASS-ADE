"""Tier a2 — assimilated method 'Signal.__post_init__'

Assimilated from: types.py:52-59
"""

from __future__ import annotations


# --- assimilated symbol ---
def __post_init__(self) -> None:
    if not self.subject.strip():
        raise ValueError("Signal.subject must be non-empty")
    if not isinstance(self.priority, Priority):
        raise TypeError("Signal.priority must be a Priority enum value")
    if not self.routes:
        raise ValueError("Signal.routes must contain at least one entry "
                         "(use ('*',) for broadcast to all)")

