"""Tier a2 — assimilated method 'FileSignalBus.broadcast'

Assimilated from: bus.py:104-123
"""

from __future__ import annotations


# --- assimilated symbol ---
def broadcast(self, signal: Signal) -> SignalEnvelope:
    """Write a signal to the inbox and log it. Returns the envelope."""
    now = self._now()
    envelope = render_envelope(
        signal,
        issued_at_compact=now.strftime("%Y%m%dT%H%M%SZ"),
        issued_at_rfc3339=now.strftime("%Y-%m-%dT%H:%M:%SZ"),
    )
    target = self.inbox_dir / f"{envelope.signal_id}.md"
    _atomic_write_text(target, serialize_envelope(envelope))
    self._append_log({
        "ts": envelope.issued_at,
        "event": "broadcast",
        "signal_id": envelope.signal_id,
        "priority": envelope.priority.value,
        "issued_by": envelope.issued_by,
        "routes": list(envelope.routes),
        "digest": envelope.digest,
    })
    return envelope

