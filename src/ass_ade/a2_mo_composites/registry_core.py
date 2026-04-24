"""Tier a2 — assimilated class 'Registry'

Assimilated from: registry.py:229-750
"""

from __future__ import annotations


# --- assimilated symbol ---
class Registry:
    """Atom store. Thread-safe for in-process access.

    Construct directly with an explicit ``path`` in tests. In production,
    :func:`default_registry` returns a module-level singleton rooted at
    the default path (``.ass-ade/registry/symbols.jsonl`` under CWD,
    overridable via ``ASS_ADE_REGISTRY_PATH``).
    """

    def __init__(
        self,
        path: Path | None = None,
        *,
        pattern_dir: Path | None = None,
        emit_genesis: bool = True,
    ):
        self._path = path or _default_registry_path()
        self._pattern_dir = pattern_dir or _leak_pattern_dir()
        self._emit_genesis = emit_genesis
        self._lock = threading.RLock()
        self._rows: dict[str, _Row] = {}
        self._load()

    # -------------------------------- persistence --------------------------

    def _load(self) -> None:
        if not self._path.exists():
            return
        with self._path.open("r", encoding="utf-8") as fh:
            for raw in fh:
                line = raw.strip()
                if not line:
                    continue
                try:
                    row = json.loads(line)
                except json.JSONDecodeError:
                    _LOGGER.warning(
                        "registry: skipping malformed JSONL row in %s", self._path
                    )
                    continue
                self._apply_row(row)

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

    def _append_row(self, row: dict[str, Any]) -> None:
        self._path.parent.mkdir(parents=True, exist_ok=True)
        line = json.dumps(row, ensure_ascii=False, separators=(",", ":"), sort_keys=True)
        with self._path.open("a", encoding="utf-8") as fh:
            fh.write(line + "\n")

    # -------------------------------- public API ---------------------------

    def lookup(
        self,
        canonical_name: str,
        version_range: str | None = None,
    ) -> Atom | None:
        """Return the Atom at ``canonical_name`` matching ``version_range``.

        ``version_range`` syntax supports three forms (kept intentionally
        small for v1; extend via ADR addendum):

        * ``None`` — any version matches.
        * ``"1.2.3"`` — exact version match.
        * ``"^1.2"`` — caret range: same major, minor ``>=`` pinned
          minor; patch unconstrained.

        Returns ``None`` if no atom matches, the atom is deprecated, or
        the version range filters it out.
        """
        with self._lock:
            row = self._rows.get(canonical_name)
            if row is None or row.deprecated:
                return None
            if version_range is None:
                return row.atom
            if not _version_matches(row.atom, version_range):
                return None
            return row.atom

    def lookup_with_metadata(
        self, canonical_name: str, version_range: str | None = None
    ) -> tuple[Atom, AtomMetadata] | None:
        """Lookup variant that also returns the scorer-facing metadata."""
        with self._lock:
            row = self._rows.get(canonical_name)
            if row is None or row.deprecated:
                return None
            if version_range is not None and not _version_matches(
                row.atom, version_range
            ):
                return None
            return row.atom, row.metadata

    def search_by_sig_fp(
        self, sig_fp_hex: str, within: float | None = None
    ) -> list[Atom]:
        """Return atoms whose ``sig_fp`` matches (exact or near).

        When ``within`` is ``None`` only exact ``sig_fp`` matches are
        returned. When provided, it is interpreted as a normalized
        Hamming distance in ``[0, 1]`` over the 64-hex-char fingerprint
        treated as a 256-bit vector: atoms with
        ``hamming_distance / 256 <= within`` match.

        The binder is the one module that should pass ``within``; it
        obtains the acceptable bound via the sovereign oracle so no
        numeric threshold is ever named in registry-internal code.
        """
        with self._lock:
            if within is None:
                return [
                    row.atom
                    for row in self._rows.values()
                    if not row.deprecated and row.atom.sig_fp == sig_fp_hex
                ]
            matches: list[Atom] = []
            target = _hex_to_bits(sig_fp_hex)
            for row in self._rows.values():
                if row.deprecated:
                    continue
                distance = _bit_distance(target, _hex_to_bits(row.atom.sig_fp))
                normalized = distance / max(1, len(target))
                if normalized <= within:
                    matches.append(row.atom)
            return matches

    def search_by_prefix(self, domain_prefix: str) -> list[Atom]:
        """Return atoms whose ``canonical_name`` starts with ``domain_prefix``."""
        with self._lock:
            return [
                row.atom
                for row in self._rows.values()
                if not row.deprecated
                and row.atom.canonical_name.startswith(domain_prefix)
            ]

    def search_by_embedding(
        self,
        query_embedding: list[float],
        k: int = 10,
    ) -> list[tuple[Atom, float]]:
        """Return the top-``k`` atoms by cosine similarity on ``embedding``.

        Additive, default-OFF lookup layer (Lane W **T-A+1** per signal
        ``20260421T045050Z-P1-reroute-wave-3-parallel-activation-enhancement-planner``).
        Does NOT change any existing registry API. Gated behind
        ``ATOMADIC_USE_EMBEDDINGS``; when the flag is unset the method
        raises :class:`EmbeddingsDisabledError` and no similarity
        computation runs. This keeps the default runtime cost exactly
        where it was before the embedding layer existed.

        ``query_embedding`` is a caller-supplied vector; the registry
        does NOT load an embedding model in-process. The caller
        (typically a future CLI `--use-embeddings` driver under Stream
        D) is responsible for producing the query vector under the
        same model used to populate ``AtomMetadata.embedding``. Keeping
        the model out of the registry's import graph means the
        embedding population lane (Wave-3+) can swap models
        (jina-code-embeddings, Voyage-code-3, CodeSage-Large) without
        touching registry.py.

        Atoms whose ``AtomMetadata.embedding`` is ``None`` are skipped
        silently: the registry's Wave-2 default leaves the column
        empty, so until a populator has run, this method returns an
        empty list rather than fabricating results.

        Deprecated atoms are skipped, matching the :meth:`iter_atoms`
        invariant.

        Returns a list of ``(atom, similarity)`` pairs, sorted by
        similarity descending, length ``<= k``. Ties are broken by
        canonical name for determinism.

        Raises:
            EmbeddingsDisabledError: when
                ``ATOMADIC_USE_EMBEDDINGS`` is not set to a truthy
                value at call time.
            EmbeddingShapeError: when any candidate atom's embedding
                has a different length than ``query_embedding``.
            ValueError: when ``k`` is not a positive integer or when
                ``query_embedding`` is empty.
        """
        if not _embeddings_enabled():
            raise EmbeddingsDisabledError(
                "registry.search_by_embedding requires ATOMADIC_USE_EMBEDDINGS "
                "to be set to a truthy value (1/true/yes/on). The feature is "
                "additive and default-off; callers that do not opt in pay "
                "zero embedding cost."
            )
        if not query_embedding:
            raise ValueError("query_embedding must be a non-empty vector")
        if not isinstance(k, int) or k <= 0:
            raise ValueError(f"k must be a positive int; got {k!r}")
        query_len = len(query_embedding)

        with self._lock:
            candidates = [
                (row.atom, row.metadata.embedding)
                for row in self._rows.values()
                if (not row.deprecated) and row.metadata.embedding is not None
            ]

        scored: list[tuple[Atom, float]] = []
        for atom, emb in candidates:
            if len(emb) != query_len:
                raise EmbeddingShapeError(
                    f"atom {atom.canonical_name!r} embedding has length "
                    f"{len(emb)}; query embedding has length {query_len}. "
                    "Re-embed the query under the model used to populate "
                    "the registry column."
                )
            scored.append((atom, _cosine_similarity(query_embedding, emb)))

        scored.sort(key=lambda pair: (-pair[1], pair[0].canonical_name))
        return scored[:k]

    def retrieve_then_rerank(
        self,
        query_embedding: list[float],
        *,
        query_sig_fp: str | None = None,
        k_retrieve: int = 50,
        within: float | None = None,
    ) -> list[tuple[Atom, float]]:
        """Two-stage candidate lookup: embedding retrieve → sig_fp narrow.

        Additive, default-OFF composition of :meth:`search_by_embedding`
        (stage 1) with a sig_fp-proximity filter (stage 2). Lane W
        **T-A+2** per the same reroute signal as T-A+1. Gated behind
        the same ``ATOMADIC_USE_EMBEDDINGS`` flag; neither the
        existing scorer entry point (``scoring.score``) nor the
        Binder's candidate-selection path is touched.

        Stage 1 — embedding retrieve. Runs
        :meth:`search_by_embedding(query_embedding, k_retrieve)` to
        collect a candidate pool of size ``<= k_retrieve``.

        Stage 2 — sig_fp narrow (optional). When ``query_sig_fp`` is
        provided, candidates are filtered to those within normalized
        Hamming distance ``within`` of ``query_sig_fp`` — the same
        metric :meth:`search_by_sig_fp` uses. ``within`` defaults to
        ``None`` which means "no narrowing" (equivalent to calling
        stage 1 alone); a caller that wants strict-contract matching
        passes a small ``within`` (the Binder receives this bound from
        the sovereign oracle per ADR-004 invariants — the registry
        does not mint it).

        Candidate ordering is preserved from stage 1 (embedding-
        similarity descending). Stage 2 is a filter, not a rescore;
        the real rerank-by-scorer lives in
        :mod:`ass_ade.engine.scoring` per ADR-008, which this
        method explicitly does NOT duplicate.

        Returns a list of ``(atom, embedding_similarity)`` pairs; the
        similarity score is carried through from stage 1 so
        downstream consumers (scorer feed, telemetry, UX) can surface
        it verbatim.

        Raises the same errors as :meth:`search_by_embedding`, plus
        ``ValueError`` if ``within`` is outside ``[0, 1]`` when
        provided.
        """
        if within is not None and not (0.0 <= within <= 1.0):
            raise ValueError(
                f"within must be in [0, 1] when provided; got {within!r}"
            )
        stage1 = self.search_by_embedding(query_embedding, k=k_retrieve)
        if query_sig_fp is None or within is None:
            return stage1
        target_bits = _hex_to_bits(query_sig_fp)
        target_len = max(1, len(target_bits))
        narrowed: list[tuple[Atom, float]] = []
        for atom, similarity in stage1:
            atom_bits = _hex_to_bits(atom.sig_fp)
            if len(atom_bits) != len(target_bits):
                continue
            distance = _bit_distance(target_bits, atom_bits)
            if distance / target_len <= within:
                narrowed.append((atom, similarity))
        return narrowed

    def iter_atoms(self, *, filter=None):
        """Stream every non-deprecated atom, lazily.

        Per ``handoffs/parent-answers-wave-2.md §5`` this is the
        canonical enumeration API for ``from_nl(..., registry_snapshot=
        iter_atoms())``. The generator is lazy and memory-bounded —
        Wave-4 sharded registries can implement the same contract
        without materializing every atom up-front.

        ``filter`` is an optional callable ``Atom -> bool``. When
        provided, only atoms where ``filter(atom)`` is truthy are
        yielded.

        Returns an iterator rather than a list: callers that need
        indexed access should call :meth:`snapshot` instead.
        """
        # Copy refs under the lock; yield outside so long-running
        # downstream iteration doesn't hold the registry open.
        with self._lock:
            atoms = [row.atom for row in self._rows.values() if not row.deprecated]
        for atom in atoms:
            if filter is not None and not filter(atom):
                continue
            yield atom

    def snapshot(self) -> list[Atom]:
        """Materialize :meth:`iter_atoms` as a list.

        Convenience wrapper for callers that need indexed access or
        multiple passes. Equivalent to ``list(self.iter_atoms())``.
        """
        return list(self.iter_atoms())

    def all_atoms(self) -> list[tuple[Atom, AtomMetadata]]:
        """Enumerate all non-deprecated atoms + metadata. Mostly for tests."""
        with self._lock:
            return [
                (row.atom, row.metadata)
                for row in self._rows.values()
                if not row.deprecated
            ]

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

    # -------------------------------- internals ----------------------------

    def _leak_check(self, atom: Atom) -> None:
        for language, body in atom.bodies.items():
            if not body.source:
                continue
            hits = scan_source_for_leaks(body.source, pattern_dir=self._pattern_dir)
            if hits:
                joined = ",".join(f"{h.category}:{h.redacted}" for h in hits)
                raise SovereignLeakError(
                    f"atom {atom.canonical_name!r} body ({language}) "
                    f"contains sovereign leak patterns: {joined}"
                )

    def _emit(self, kind: str, atom: Atom) -> None:
        if not self._emit_genesis:
            return
        try:
            from ass_ade.sovereign.genesis_log import emit_event

            emit_event(
                phase="binder",
                kind="decision",
                input={
                    "op": kind,
                    "canonical_name": atom.canonical_name,
                },
                output={
                    "sig_fp": atom.sig_fp,
                    "version": f"{atom.version_major}.{atom.version_minor}.{atom.version_patch}",
                    "languages": sorted(atom.bodies.keys()),
                },
                verdict="success",
                tags=("registry", kind),
                sovereign=False,
            )
        except Exception:
            _LOGGER.debug("registry genesis emit failed", exc_info=True)

