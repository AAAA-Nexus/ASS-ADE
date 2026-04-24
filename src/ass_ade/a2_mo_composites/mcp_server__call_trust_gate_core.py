"""Tier a2 — assimilated method 'MCPServer._call_trust_gate'

Assimilated from: server.py:1377-1408
"""

from __future__ import annotations


# --- assimilated symbol ---
def _call_trust_gate(
    self,
    req_id: Any,
    args: dict[str, Any],
    token: Any = None,
    cancellation_context: CancellationContext | None = None,
) -> dict[str, Any]:
    agent_id = args.get("agent_id", "")
    if not agent_id:
        return self._error(req_id, -32602, "agent_id is required")
    self._emit_progress(token, 0.0, message="Starting trust gate evaluation...")

    # Cancellation checkpoint
    if cancellation_context and cancellation_context.check():
        return self._error(req_id, -32800, "Request cancelled")

    from ass_ade.workflows import trust_gate

    client = self._get_nexus_client()
    self._emit_progress(token, 0.2, message="Verifying identity...")
    with client:
        self._emit_progress(token, 0.5, message="Running trust pipeline...")
        result = trust_gate(client, agent_id)
    self._emit_progress(token, 1.0, message="Trust gate complete.")
    text = json.dumps(result.model_dump(), indent=2)
    return self._result(
        req_id,
        {
            "content": [{"type": "text", "text": text}],
            "isError": result.verdict == "DENY",
        },
    )

