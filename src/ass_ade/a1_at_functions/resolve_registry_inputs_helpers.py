"""Tier a1 — assimilated function 'resolve_registry_inputs'

Assimilated from: rebuild/orchestrator.py:60-123
"""

from __future__ import annotations


# --- assimilated symbol ---
def resolve_registry_inputs(
    registry: list[dict[str, Any]] | list[Atom] | None,
    *,
    use_default_registry: bool = True,
) -> tuple[list[dict[str, Any]], list[Atom]]:
    """Normalize rebuild registry inputs for gap matching and CNA collisions.

    Rebuild historically consumed dict-like component records for ingest and
    gap-fill, while CNA expects real Atom rows for collision checks. This helper
    preserves the old dict path and lets callers opt into registry-backed CNA
    checks by passing either component records or Atom snapshots explicitly.
    """
    if registry is None:
        if use_default_registry:
            try:
                from ass_ade.engine.registry import default_registry

                raw_entries: list[Any] = list(default_registry().snapshot())
            except Exception:
                raw_entries = []
        else:
            raw_entries = []
    else:
        raw_entries = list(registry)

    component_records: list[dict[str, Any]] = []
    atom_candidates: list[Atom] = []
    for entry in raw_entries:
        if isinstance(entry, Atom):
            atom_candidates.append(entry)
            component_records.append(
                {
                    "id": entry.canonical_name,
                    "name": entry.canonical_name.rsplit(".", 1)[-1],
                    "tier": entry.tier,
                }
            )
            continue
        if isinstance(entry, dict):
            canonical_name = entry.get("id") or entry.get("canonical_name")
            if not canonical_name:
                continue
            record = dict(entry)
            record["id"] = str(canonical_name)
            record.setdefault(
                "name",
                str(record.get("name") or str(canonical_name).rsplit(".", 1)[-1]),
            )
            component_records.append(record)
            atom_candidates.append(
                Atom(
                    canonical_name=record["id"],
                    tier=str(record.get("tier") or str(record["id"]).split(".", 1)[0] or "a1"),
                    domain="op",
                    sovereign=bool(record.get("sovereign", False)),
                    sig_fp=str(record.get("sig_fp") or ("0" * 64)),
                    version_major=int(record.get("version_major", 0) or 0),
                    version_minor=int(record.get("version_minor", 0) or 0),
                    version_patch=int(record.get("version_patch", 0) or 0),
                    bodies={},
                )
            )

    return component_records, atom_candidates

