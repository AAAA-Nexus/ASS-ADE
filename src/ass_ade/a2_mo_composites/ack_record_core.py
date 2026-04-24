"""Tier a2 — assimilated class 'AckRecord'

Assimilated from: types.py:90-96
"""

from __future__ import annotations


# --- assimilated symbol ---
class AckRecord:
    """Acknowledgement written by an agent after handling a signal."""

    signal_id: str
    ack_by: str
    ack_at: str
    note: str = ""

