"""Tier a2 — assimilated method 'AtomMetadata.to_dict'

Assimilated from: types.py:115-126
"""

from __future__ import annotations


# --- assimilated symbol ---
def to_dict(self) -> dict:
    return {
        "created_at": self.created_at.isoformat(),
        "last_success_at": (
            self.last_success_at.isoformat()
            if self.last_success_at is not None
            else None
        ),
        "perf_percentile": self.perf_percentile,
        "provenance_multi_source_score": self.provenance_multi_source_score,
        "embedding": self.embedding,
    }

