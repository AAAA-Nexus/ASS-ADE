"""Tier a2 — assimilated method 'FileSignalBus.unread'

Assimilated from: bus.py:142-169
"""

from __future__ import annotations


# --- assimilated symbol ---
def unread(self) -> list[DeliveryReceipt]:
    """Return signals routed to this agent that have not been delivered yet.

    Side-effect: each returned signal is marked as delivered for the
    current ``agent_id`` so a subsequent call returns an empty list unless
    a new broadcast has landed. Use ``peek`` for a side-effect-free read.
    """
    now_iso = _rfc3339(self._now())
    receipts: list[DeliveryReceipt] = []
    for env in self.list_inbox():
        if not env.matches(self.agent_id):
            continue
        if env.is_expired(now_iso):
            continue
        marker = self._delivery_marker(env.signal_id)
        already = marker.exists()
        if already:
            continue
        _atomic_write_text(marker, now_iso + "\n")
        self._append_log({
            "ts": now_iso, "event": "delivered",
            "agent": self.agent_id, "signal_id": env.signal_id,
            "priority": env.priority.value,
        })
        receipts.append(DeliveryReceipt(envelope=env,
                                        was_delivered_before=False,
                                        delivered_to=self.agent_id))
    return receipts

