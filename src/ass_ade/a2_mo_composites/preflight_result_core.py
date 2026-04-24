"""Tier a2 — assimilated class 'PreflightResult'

Assimilated from: nexus.py:120-137
"""

from __future__ import annotations


# --- assimilated symbol ---
class PreflightResult:
    """Nexus preflight receipts attached to inbound envelope.

    The full shape mirrors ``_PROTOCOL.md §11.1`` minus the sovereign
    ``ceiling`` handle (that lives on :class:`TrustReceipt`). Each
    field is a handle or a coarse verdict; raw scan inputs and drift
    sources are NOT retained here.
    """

    aegis_receipt_id: str
    aegis_verdict: str  # "clean" | "suspicious" | "blocked"
    drift_receipt_id: str
    drift_verdict: str  # "fresh" | "stale" | "missing_source"
    bound_to: str  # sha256 of canonical(inputs)
    ts: str

    def clean(self) -> bool:
        return self.aegis_verdict == "clean" and self.drift_verdict == "fresh"

