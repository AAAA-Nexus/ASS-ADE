"""Tier a2 — assimilated class 'BinderRefused'

Assimilated from: nexus.py:95-111
"""

from __future__ import annotations


# --- assimilated symbol ---
class BinderRefused(NexusError):
    """Binder refused a manifest because a Nexus check fired.

    ``code`` matches the ``refusal_kind`` enum in ``_PROTOCOL.md
    §11.5`` with a ``nexus_`` prefix on non-prefixed kinds. Callers
    pattern-match on ``code``:

    - ``nexus_injection_blocked`` (Aegis-Edge verdict != clean)
    - ``nexus_drift_stale`` (UEP-govern verdict != fresh)
    - ``hallucination_ceiling_exceeded`` (postflight oracle above ceiling)
    - ``nexus_preflight_missing`` (inbound envelope lacks receipts)
    - ``session_ratchet_stale`` (session epoch behind Nexus)
    """

    def __init__(self, code: str, message: str = ""):
        self.code = code
        super().__init__(message or code)

