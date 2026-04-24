"""Tier a1 — assimilated function 'search_by_embedding'

Assimilated from: registry.py:800-808
"""

from __future__ import annotations


# --- assimilated symbol ---
def search_by_embedding(
    query_embedding: list[float], k: int = 10
) -> list[tuple[Atom, float]]:
    """Module-level convenience wrapper over :meth:`Registry.search_by_embedding`.

    Gated by ``ATOMADIC_USE_EMBEDDINGS``; raises
    :class:`EmbeddingsDisabledError` when the flag is unset.
    """
    return default_registry().search_by_embedding(query_embedding, k=k)

