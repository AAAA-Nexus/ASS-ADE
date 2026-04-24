"""Tier a2 — assimilated method 'Registry._apply_row'

Assimilated from: registry.py:271-305
"""

from __future__ import annotations


# --- assimilated symbol ---
def _apply_row(self, row: dict[str, Any]) -> None:
    op = row.get("op")
    if op == "register":
        atom = _atom_from_dict(row["atom"])
        metadata = AtomMetadata.from_dict(row.get("metadata", {}))
        self._rows[atom.canonical_name] = _Row(atom=atom, metadata=metadata)
    elif op == "metadata":
        name = row["atom_ref"]["canonical_name"]
        current = self._rows.get(name)
        if current is None:
            _LOGGER.warning(
                "registry: metadata row references unknown atom %s", name
            )
            return
        updates = row.get("updates", {})
        delta = updates.get("usage_count_delta")
        if isinstance(delta, int):
            current.atom.usage_count += delta
        trust = updates.get("trust_score")
        if isinstance(trust, (int, float)):
            current.atom.trust_score = float(trust)
        deprecated = updates.get("deprecated")
        if deprecated is not None:
            current.deprecated = bool(deprecated)
            current.deprecation_reason = updates.get("deprecation_reason")
        last_success = updates.get("last_success_at")
        if isinstance(last_success, str):
            current.metadata.last_success_at = datetime.fromisoformat(
                last_success
            )
        perf = updates.get("perf_percentile")
        if isinstance(perf, (int, float)):
            current.metadata.perf_percentile = float(perf)
    else:
        _LOGGER.warning("registry: unknown op %r in row", op)

