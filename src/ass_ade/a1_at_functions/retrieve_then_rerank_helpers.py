"""Tier a1 — assimilated function 'retrieve_then_rerank'

Assimilated from: registry.py:811-828
"""

from __future__ import annotations


# --- assimilated symbol ---
def retrieve_then_rerank(
    query_embedding: list[float],
    *,
    query_sig_fp: str | None = None,
    k_retrieve: int = 50,
    within: float | None = None,
) -> list[tuple[Atom, float]]:
    """Module-level convenience wrapper over :meth:`Registry.retrieve_then_rerank`.

    Gated by ``ATOMADIC_USE_EMBEDDINGS``; raises
    :class:`EmbeddingsDisabledError` when the flag is unset.
    """
    return default_registry().retrieve_then_rerank(
        query_embedding,
        query_sig_fp=query_sig_fp,
        k_retrieve=k_retrieve,
        within=within,
    )

