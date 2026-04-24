"""Tier a2 — assimilated method 'MCPServer._handle_tools_call'

Assimilated from: server.py:856-933
"""

from __future__ import annotations


# --- assimilated symbol ---
def _handle_tools_call(self, req_id: Any, params: dict[str, Any]) -> dict[str, Any]:
    # Check if this request was already cancelled
    with self._lock:
        if req_id in self._cancelled:
            self._cancelled.discard(req_id)
            return self._error(req_id, -32800, "Request cancelled")
        # Create a cancellation context for this request
        ctx = CancellationContext()
        self._cancellation_contexts[req_id] = ctx

    try:
        name = params.get("name", "")
        arguments = params.get("arguments") or {}

        # MCP 2025-11-25: extract progress token from _meta
        meta = params.get("_meta") or {}
        progress_token: Any = meta.get("progressToken")

        # Route workflow / agent / A2A tools
        workflow_names = {t["name"] for t in _WORKFLOW_TOOLS}
        if name in workflow_names:
            return self._handle_extended_call(
                req_id, name, arguments, progress_token, ctx
            )

        # Phase 2: pre-execution NCB gate for write/edit tools
        allow, reason = self._pre_tool_hook(name, arguments)
        if not allow:
            return self._result(
                req_id,
                {
                    "content": [{"type": "text", "text": reason}],
                    "isError": True,
                },
            )

        # Snapshot pre-write content so LoRA gets a real bad→good sample
        pre_write_content = ""
        if name in ("write_file", "edit_file"):
            snap_path = arguments.get("path") or arguments.get("file_path")
            if snap_path:
                try:
                    from pathlib import Path as _P

                    p = _P(snap_path)
                    if p.exists() and p.is_file() and p.stat().st_size < 512_000:
                        pre_write_content = p.read_text(
                            encoding="utf-8", errors="replace"
                        )
                except (OSError, RuntimeError, TypeError, ValueError):
                    pass

        result = self._registry.execute(name, **arguments)

        # Phase 2/3/5: post-execution gates (TCA record, CIE validate, LoRA capture)
        result = self._post_tool_hook(
            name, arguments, result, pre_write_content=pre_write_content
        )

        content: list[dict[str, str]] = []
        if result.success:
            content.append({"type": "text", "text": result.output})
        else:
            content.append(
                {"type": "text", "text": result.error or "Unknown error"}
            )

        return self._result(
            req_id,
            {
                "content": content,
                "isError": not result.success,
            },
        )
    finally:
        # Clean up cancellation context
        with self._lock:
            self._cancellation_contexts.pop(req_id, None)

