"""Tier a2 — assimilated method 'Registry.search_by_embedding'

Assimilated from: registry.py:400-478
"""

from __future__ import annotations


# --- assimilated symbol ---
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

