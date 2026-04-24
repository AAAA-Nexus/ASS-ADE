"""Tier a1 — assimilated function 'serialize_envelope'

Assimilated from: protocol.py:79-97
"""

from __future__ import annotations


# --- assimilated symbol ---
def serialize_envelope(env: SignalEnvelope) -> str:
    """Render an envelope as the canonical on-disk markdown."""
    lines = ["---"]
    lines.append(f"signal_id: {env.signal_id}")
    lines.append(f"priority: {env.priority.value}")
    lines.append(f"issued_by: {env.issued_by}")
    lines.append(f"issued_at: {env.issued_at}")
    lines.append(f"subject: {env.subject}")
    lines.append("routes:")
    for r in env.routes:
        lines.append(f"  - {r}")
    lines.append(f"ack_required: {'true' if env.ack_required else 'false'}")
    lines.append(f"expires_at: {env.expires_at}")
    lines.append(f"digest: {env.digest}")
    lines.append("---")
    lines.append("")
    lines.append(env.body.rstrip())
    lines.append("")
    return "\n".join(lines)

