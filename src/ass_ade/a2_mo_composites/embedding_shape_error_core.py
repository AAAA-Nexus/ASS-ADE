"""Tier a2 — assimilated class 'EmbeddingShapeError'

Assimilated from: types.py:372-380
"""

from __future__ import annotations


# --- assimilated symbol ---
class EmbeddingShapeError(EngineError):
    """Query embedding shape does not match any registered atom embedding.

    Raised by :meth:`Registry.search_by_embedding` when the query
    embedding's length differs from the stored atom embeddings,
    which would make cosine similarity ill-defined. The caller
    (typically a Binder pre-processor) must re-embed the query under
    the same model used to populate the registry column.
    """

