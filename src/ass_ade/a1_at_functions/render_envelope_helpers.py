"""Tier a1 — assimilated function 'render_envelope'

Assimilated from: protocol.py:52-76
"""

from __future__ import annotations


# --- assimilated symbol ---
def render_envelope(
    signal: Signal,
    *,
    issued_at_compact: str,
    issued_at_rfc3339: str,
) -> SignalEnvelope:
    """Build a wire-ready ``SignalEnvelope`` from a logical ``Signal``.

    Caller supplies timestamps so the function stays pure; the bus layer owns
    the clock.
    """
    sid = signal_id_for(signal.priority, signal.subject, issued_at_compact)
    return SignalEnvelope(
        signal_id=sid,
        priority=signal.priority,
        issued_by=signal.issued_by,
        issued_at=issued_at_rfc3339,
        subject=signal.subject.strip(),
        body=signal.body.strip(),
        routes=tuple(signal.routes),
        ack_required=signal.ack_required,
        expires_at=signal.expires_at,
        digest=_digest(sid, signal.subject.strip(), signal.body.strip(),
                       signal.issued_by),
    )

