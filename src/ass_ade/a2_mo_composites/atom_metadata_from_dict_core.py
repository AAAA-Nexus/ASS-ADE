"""Tier a2 — assimilated method 'AtomMetadata.from_dict'

Assimilated from: types.py:129-142
"""

from __future__ import annotations


# --- assimilated symbol ---
def from_dict(cls, data: dict) -> AtomMetadata:
    def _parse(iso: str | None) -> datetime | None:
        if iso is None:
            return None
        return datetime.fromisoformat(iso)

    created = _parse(data.get("created_at"))
    return cls(
        created_at=created or datetime.now(UTC),
        last_success_at=_parse(data.get("last_success_at")),
        perf_percentile=data.get("perf_percentile"),
        provenance_multi_source_score=data.get("provenance_multi_source_score"),
        embedding=data.get("embedding"),
    )

