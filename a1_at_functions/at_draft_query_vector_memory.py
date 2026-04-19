# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a1_at_functions/at_draft_query_vector_memory.py:7
# Component id: at.source.a1_at_functions.query_vector_memory
from __future__ import annotations

__version__ = "0.1.0"

def query_vector_memory(
    *,
    query: str,
    namespace: str = "default",
    top_k: int = 5,
    working_dir: str | Path = ".",
) -> VectorMemoryQueryResult:
    """Return nearest local vector memories for a query."""
    if not query.strip():
        raise ValueError("query must not be empty")
    namespace = namespace.strip() or "default"
    top_k = max(1, min(int(top_k), 25))

    query_vector = vector_embed(query)
    scored: list[tuple[float, VectorMemoryRecord]] = []
    for record in _iter_memory(_memory_path(working_dir)):
        if record.namespace != namespace:
            continue
        scored.append((_dot(query_vector, record.vector), record))

    scored.sort(key=lambda item: item[0], reverse=True)
    matches = [
        VectorMemoryMatch(
            id=record.id,
            namespace=record.namespace,
            score=round(score, 6),
            text=record.text,
            metadata=record.metadata,
            created_at=record.created_at,
        )
        for score, record in scored[:top_k]
    ]
    return VectorMemoryQueryResult(
        query=query,
        namespace=namespace,
        matches=matches,
    )
