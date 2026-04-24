"""Tier a2 — assimilated method 'Registry.update_metadata'

Assimilated from: registry.py:662-711
"""

from __future__ import annotations


# --- assimilated symbol ---
def update_metadata(
    self,
    atom_ref: AtomRef,
    *,
    usage_count_delta: int | None = None,
    trust_score: float | None = None,
    deprecated: bool | None = None,
    deprecation_reason: str | None = None,
    last_success_at: datetime | None = None,
    perf_percentile: float | None = None,
) -> None:
    """Mutate an atom's metadata. Registry is still append-only —
    the change is a new JSONL row that supersedes any earlier
    metadata value.
    """
    with self._lock:
        row = self._rows.get(atom_ref.canonical_name)
        if row is None:
            raise KeyError(
                f"atom {atom_ref.canonical_name!r} not in registry"
            )
        updates: dict[str, Any] = {}
        if usage_count_delta is not None:
            row.atom.usage_count += int(usage_count_delta)
            updates["usage_count_delta"] = int(usage_count_delta)
        if trust_score is not None:
            row.atom.trust_score = float(trust_score)
            updates["trust_score"] = float(trust_score)
        if deprecated is not None:
            row.deprecated = bool(deprecated)
            updates["deprecated"] = bool(deprecated)
            if deprecation_reason is not None:
                row.deprecation_reason = deprecation_reason
                updates["deprecation_reason"] = deprecation_reason
        if last_success_at is not None:
            row.metadata.last_success_at = last_success_at
            updates["last_success_at"] = last_success_at.isoformat()
        if perf_percentile is not None:
            row.metadata.perf_percentile = float(perf_percentile)
            updates["perf_percentile"] = float(perf_percentile)
        if not updates:
            return
        row_payload = {
            "op": "metadata",
            "ts": _utc_now_iso(),
            "atom_ref": _atomref_to_dict(atom_ref),
            "updates": updates,
        }
        self._append_row(row_payload)
        self._emit("metadata_updated", row.atom)

