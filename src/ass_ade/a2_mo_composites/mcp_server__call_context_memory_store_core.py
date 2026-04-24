"""Tier a2 — assimilated method 'MCPServer._call_context_memory_store'

Assimilated from: server.py:1293-1329
"""

from __future__ import annotations


# --- assimilated symbol ---
def _call_context_memory_store(
    self,
    req_id: Any,
    args: dict[str, Any],
    token: Any = None,
    cancellation_context: CancellationContext | None = None,
) -> dict[str, Any]:
    text_value = args.get("text", "")
    if not text_value:
        return self._error(req_id, -32602, "text is required")
    metadata = args.get("metadata") or {}
    if not isinstance(metadata, dict):
        return self._error(req_id, -32602, "metadata must be an object")

    self._emit_progress(token, 0.0, message="Storing vector memory...")

    # Cancellation checkpoint
    if cancellation_context and cancellation_context.check():
        return self._error(req_id, -32800, "Request cancelled")

    from ass_ade.context_memory import store_vector_memory

    result = store_vector_memory(
        text=str(text_value),
        namespace=str(args.get("namespace") or "default"),
        metadata=metadata,
        working_dir=self._working_dir,
    )
    self._emit_progress(token, 1.0, message="Vector memory stored.")
    text = json.dumps(result.model_dump(), indent=2)
    return self._result(
        req_id,
        {
            "content": [{"type": "text", "text": text}],
            "isError": False,
        },
    )

