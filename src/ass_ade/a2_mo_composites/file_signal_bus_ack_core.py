"""Tier a2 — assimilated method 'FileSignalBus.ack'

Assimilated from: bus.py:187-211
"""

from __future__ import annotations


# --- assimilated symbol ---
def ack(self, signal_id: str, note: str = "") -> AckRecord:
    """Persist an acknowledgement for ``signal_id`` under this agent."""
    record = AckRecord(
        signal_id=signal_id,
        ack_by=self.agent_id,
        ack_at=_rfc3339(self._now()),
        note=note.strip(),
    )
    ack_path = self._ack_path(signal_id)
    content = (
        "---\n"
        f"signal_id: {record.signal_id}\n"
        f"ack_by: {record.ack_by}\n"
        f"ack_at: {record.ack_at}\n"
        "---\n"
        "\n"
        f"{record.note}\n"
    )
    _atomic_write_text(ack_path, content)
    self._append_log({
        "ts": record.ack_at, "event": "ack",
        "agent": record.ack_by, "signal_id": record.signal_id,
        "note": record.note,
    })
    return record

