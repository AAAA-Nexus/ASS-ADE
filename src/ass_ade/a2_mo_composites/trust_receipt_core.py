"""Tier a2 — assimilated class 'TrustReceipt'

Assimilated from: nexus.py:141-158
"""

from __future__ import annotations


# --- assimilated symbol ---
class TrustReceipt:
    """Nexus postflight receipt attached to :class:`BindPlan`.

    ``signed_over`` is the sha256 of the outbound ``result`` payload;
    the parent agent verifies the ratchet signature on receipt. The
    hallucination ``ceiling`` handle is opaque — the sovereign value
    is never materialized on this side of the wire.
    """

    hallucination_receipt_id: str
    hallucination_verdict: str  # "within_ceiling" | "above_ceiling" | "unverifiable"
    ceiling_handle: str
    claims_checked: int
    trust_chain_receipt_id: str
    signed_over: str  # sha256 of canonical(result)
    ratchet_epoch: int
    principal: str
    ts: str

