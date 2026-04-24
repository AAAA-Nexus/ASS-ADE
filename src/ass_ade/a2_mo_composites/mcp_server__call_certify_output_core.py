"""Tier a2 — assimilated method 'MCPServer._call_certify_output'

Assimilated from: server.py:1410-1443
"""

from __future__ import annotations


# --- assimilated symbol ---
def _call_certify_output(
    self,
    req_id: Any,
    args: dict[str, Any],
    token: Any = None,
    cancellation_context: CancellationContext | None = None,
) -> dict[str, Any]:
    text = args.get("text", "")
    if not text:
        return self._error(req_id, -32602, "text is required")
    self._emit_progress(token, 0.0, message="Starting output certification...")

    # Cancellation checkpoint
    if cancellation_context and cancellation_context.check():
        return self._error(req_id, -32800, "Request cancelled")

    from ass_ade.workflows import certify_output

    client = self._get_nexus_client()
    self._emit_progress(token, 0.2, message="Running hallucination oracle...")
    with client:
        self._emit_progress(
            token, 0.5, message="Running ethics and compliance checks..."
        )
        result = certify_output(client, text)
    self._emit_progress(token, 1.0, message="Certification complete.")
    out = json.dumps(result.model_dump(), indent=2)
    return self._result(
        req_id,
        {
            "content": [{"type": "text", "text": out}],
            "isError": not result.passed,
        },
    )

