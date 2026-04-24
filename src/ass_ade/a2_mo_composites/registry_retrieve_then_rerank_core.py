"""Tier a2 — assimilated method 'Registry.retrieve_then_rerank'

Assimilated from: registry.py:480-543
"""

from __future__ import annotations


# --- assimilated symbol ---
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

