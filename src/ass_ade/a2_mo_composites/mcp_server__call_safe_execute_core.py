"""Tier a2 — assimilated method 'MCPServer._call_safe_execute'

Assimilated from: server.py:1445-1486
"""

from __future__ import annotations


# --- assimilated symbol ---
def _call_safe_execute(
    self,
    req_id: Any,
    args: dict[str, Any],
    token: Any = None,
    cancellation_context: CancellationContext | None = None,
) -> dict[str, Any]:
    tool_name = args.get("tool_name", "")
    tool_input_str = args.get("tool_input", "{}")
    if not tool_name:
        return self._error(req_id, -32602, "tool_name is required")
    try:
        if isinstance(tool_input_str, str):
            tool_input = json.loads(tool_input_str)
        else:
            tool_input = tool_input_str
    except json.JSONDecodeError:
        return self._error(req_id, -32602, "tool_input must be valid JSON")
    self._emit_progress(token, 0.0, message="Starting AEGIS safe execute...")

    # Cancellation checkpoint
    if cancellation_context and cancellation_context.check():
        return self._error(req_id, -32800, "Request cancelled")

    from ass_ade.workflows import safe_execute

    client = self._get_nexus_client()
    self._emit_progress(
        token, 0.3, message="Running security shield and prompt scan..."
    )
    with client:
        self._emit_progress(token, 0.6, message="Executing via AEGIS proxy...")
        result = safe_execute(client, tool_name, tool_input)
    self._emit_progress(token, 1.0, message="Safe execute complete.")
    out = json.dumps(result.model_dump(), indent=2)
    return self._result(
        req_id,
        {
            "content": [{"type": "text", "text": out}],
            "isError": not result.shield_passed,
        },
    )

