"""Tier a2 — assimilated class 'AtomMetadata'

Assimilated from: types.py:88-142
"""

from __future__ import annotations


# --- assimilated symbol ---
class AtomMetadata:
    """Scorer-facing ancillary data for an atom.

    The public `Atom` (from Stream C) is intentionally minimal. Fields
    the scorer needs — creation timestamp (for recency), last-successful
    signal (for recency tiebreak), per-language performance percentile
    (for `m_perf`), and cross-source provenance count (for `m_prov`) —
    live here. The registry persists these alongside the Atom in the
    JSONL row and hands them back to the scorer. Missing fields are
    treated as neutral per the Scorer (12) contract, not fabricated.

    `embedding` is a Wave-2 reserve field for Lane W **T-A+2** (embedding
    column populator). Kept on `AtomMetadata` rather than the public
    `Atom` to keep the public manifest surface minimal and to avoid a
    cross-stream edit of `capability.types`. Default is `None`; no writer
    populates it in Wave 2. When Lane W ships, the populator writes into
    this field and the registry round-trips it transparently.
    """

    created_at: datetime = field(
        default_factory=lambda: datetime.now(UTC)
    )
    last_success_at: datetime | None = None
    perf_percentile: float | None = None
    provenance_multi_source_score: float | None = None
    embedding: list[float] | None = None

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

    @classmethod
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

