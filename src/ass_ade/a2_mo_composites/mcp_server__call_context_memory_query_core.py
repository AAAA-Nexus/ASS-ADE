"""Tier a2 — assimilated method 'MCPServer._call_context_memory_query'

Assimilated from: server.py:1331-1375
"""

from __future__ import annotations


# --- assimilated symbol ---
def _call_context_memory_query(
    self,
    req_id: Any,
    args: dict[str, Any],
    token: Any = None,
    cancellation_context: CancellationContext | None = None,
) -> dict[str, Any]:
    query = args.get("query", "")
    if not query:
        return self._error(req_id, -32602, "query is required")

    self._emit_progress(token, 0.0, message="Querying vector memory...")

    # Cancellation checkpoint
    if cancellation_context and cancellation_context.check():
        return self._error(req_id, -32800, "Request cancelled")

    from ass_ade.context_memory import query_vector_memory

    raw_min = args.get("min_score", None)
    min_score: float | None
    if raw_min is None or raw_min == "":
        min_score = None
    else:
        try:
            min_score = float(raw_min)
        except (TypeError, ValueError):
            return self._error(req_id, -32602, "min_score must be a number")

    result = query_vector_memory(
        query=str(query),
        namespace=str(args.get("namespace") or "default"),
        top_k=int(args.get("top_k", 5)),
        working_dir=self._working_dir,
        min_score=min_score,
    )
    self._emit_progress(token, 1.0, message="Vector memory query complete.")
    text = json.dumps(result.model_dump(), indent=2)
    return self._result(
        req_id,
        {
            "content": [{"type": "text", "text": text}],
            "isError": False,
        },
    )

