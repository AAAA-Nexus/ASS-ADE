"""Tier a2 — assimilated method 'Priority.parse'

Assimilated from: types.py:21-28
"""

from __future__ import annotations


# --- assimilated symbol ---
def parse(cls, value: str) -> Priority:
    try:
        return cls(value)
    except ValueError as e:
        raise ValueError(
            f"unknown priority '{value}'; expected one of "
            f"{[p.value for p in cls]}"
        ) from e

