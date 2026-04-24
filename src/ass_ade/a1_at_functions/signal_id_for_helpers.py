"""Tier a1 — assimilated function 'signal_id_for'

Assimilated from: protocol.py:39-49
"""

from __future__ import annotations


# --- assimilated symbol ---
def signal_id_for(priority: Priority, subject: str, issued_at_compact: str) -> str:
    """Compose a signal id from its key inputs.

    ``issued_at_compact`` must already be formatted as ``YYYYMMDDTHHMMSSZ``.
    Pure so that tests can pin ids without stubbing the clock.
    """
    if not _SIGNAL_ID_RE.match(f"{issued_at_compact}-{priority.value}-stub"):
        raise ValueError(
            f"issued_at_compact must be YYYYMMDDTHHMMSSZ, got {issued_at_compact!r}"
        )
    return f"{issued_at_compact}-{priority.value}-{_slugify(subject)}"

