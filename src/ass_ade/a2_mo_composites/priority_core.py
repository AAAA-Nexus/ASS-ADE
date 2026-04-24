"""Tier a2 — assimilated class 'Priority'

Assimilated from: types.py:12-33
"""

from __future__ import annotations


# --- assimilated symbol ---
class Priority(StrEnum):
    """Signal priority. Ordering is strict: P0 halts, P3 is low-noise FYI."""

    P0_HALT = "P0-halt"
    P1_REROUTE = "P1-reroute"
    P2_INFORM = "P2-inform"
    P3_FYI = "P3-fyi"

    @classmethod
    def parse(cls, value: str) -> Priority:
        try:
            return cls(value)
        except ValueError as e:
            raise ValueError(
                f"unknown priority '{value}'; expected one of "
                f"{[p.value for p in cls]}"
            ) from e

    @property
    def rank(self) -> int:
        """Lower rank = higher urgency. Used for inbox ordering."""
        return {"P0-halt": 0, "P1-reroute": 1, "P2-inform": 2, "P3-fyi": 3}[self.value]

