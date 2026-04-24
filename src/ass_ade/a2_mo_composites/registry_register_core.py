"""Tier a2 — assimilated method 'Registry.register'

Assimilated from: registry.py:587-660
"""

from __future__ import annotations


# --- assimilated symbol ---
def register(
    self,
    atom: Atom,
    *,
    metadata: AtomMetadata | None = None,
    verify_fingerprints: bool = True,
) -> AtomRef:
    """Register a new atom. Raises on violations.

    Checks performed, in order:

    1. Every body's ``source`` is scanned against the sovereign
       leak corpus. Any hit → :class:`SovereignLeakError` (atom
       is not persisted).
    2. When ``verify_fingerprints`` is true (the default),
       ``atom.sig_fp`` and each body's ``body_fp`` are recomputed
       from ``body.source`` and compared to the claimed values.
       Mismatch → :class:`ValueError` (tampered atom).
    3. If the canonical name already exists:

       * same ``sig_fp`` — polyglot body additions and
         metadata-style fields are merged. Bodies in the existing
         atom are preserved unless ``atom`` supplies a replacement
         at the same language (in which case the newer body wins
         and triggers a patch-level bump if the body_fp differs,
         otherwise the write is an idempotent no-op).
       * different ``sig_fp`` — contract break. Raises
         :class:`AtomCollisionError`. Caller must produce a new
         canonical name or explicitly bump the major version
         before re-submitting.

    Returns the registered :class:`AtomRef`.
    """
    with self._lock:
        self._leak_check(atom)
        if verify_fingerprints:
            _verify_fingerprints(atom)
        existing = self._rows.get(atom.canonical_name)
        if existing is None:
            meta = metadata or AtomMetadata()
            self._rows[atom.canonical_name] = _Row(atom=atom, metadata=meta)
            row_payload = {
                "op": "register",
                "ts": _utc_now_iso(),
                "atom": _atom_to_dict(atom),
                "metadata": meta.to_dict(),
            }
            self._append_row(row_payload)
            self._emit("registered", atom)
            return AtomRef.from_atom(atom)
        if existing.atom.sig_fp != atom.sig_fp:
            raise AtomCollisionError(
                f"canonical_name {atom.canonical_name!r} already registered with "
                f"different sig_fp; caller must bump major version or pick a new name."
            )
        merged = _merge_bodies(existing.atom, atom)
        merged_meta = existing.metadata
        if metadata is not None:
            merged_meta = _merge_metadata(existing.metadata, metadata)
        self._rows[atom.canonical_name] = _Row(
            atom=merged,
            metadata=merged_meta,
            deprecated=existing.deprecated,
            deprecation_reason=existing.deprecation_reason,
        )
        row_payload = {
            "op": "register",
            "ts": _utc_now_iso(),
            "atom": _atom_to_dict(merged),
            "metadata": merged_meta.to_dict(),
        }
        self._append_row(row_payload)
        self._emit("polyglot_body_added", merged)
        return AtomRef.from_atom(merged)

