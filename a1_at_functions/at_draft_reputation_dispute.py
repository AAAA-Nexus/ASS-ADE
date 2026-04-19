# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a1_at_functions/at_draft_reputation_dispute.py:7
# Component id: at.source.a1_at_functions.reputation_dispute
from __future__ import annotations

__version__ = "0.1.0"

def reputation_dispute(self, entry_id: str, reason: str, **kwargs: Any) -> dict:
    """/v1/reputation/dispute — challenge an entry. $0.080/call"""
    return self._post_raw("/v1/reputation/dispute", {"entry_id": entry_id, "reason": reason, **kwargs})
