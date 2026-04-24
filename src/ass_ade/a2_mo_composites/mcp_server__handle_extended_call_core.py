"""Tier a2 — assimilated method 'MCPServer._handle_extended_call'

Assimilated from: server.py:935-1004
"""

from __future__ import annotations


# --- assimilated symbol ---
def _handle_extended_call(
    self,
    req_id: Any,
    name: str,
    arguments: dict[str, Any],
    progress_token: Any = None,
    cancellation_context: CancellationContext | None = None,
) -> dict[str, Any]:
    """Handle workflow, agent, and A2A tool calls with optional progress reporting and cancellation."""
    try:
        if name == "phase0_recon":
            return self._call_phase0_recon(
                req_id, arguments, progress_token, cancellation_context
            )
        elif name == "epiphany_breakthrough_cycle":
            return self._call_epiphany_breakthrough_cycle(
                req_id, arguments, progress_token, cancellation_context
            )
        elif name == "context_pack":
            return self._call_context_pack(
                req_id, arguments, progress_token, cancellation_context
            )
        elif name == "context_memory_store":
            return self._call_context_memory_store(
                req_id, arguments, progress_token, cancellation_context
            )
        elif name == "context_memory_query":
            return self._call_context_memory_query(
                req_id, arguments, progress_token, cancellation_context
            )
        elif name == "map_terrain":
            return self._call_map_terrain(
                req_id, arguments, progress_token, cancellation_context
            )
        elif name == "trust_gate":
            return self._call_trust_gate(
                req_id, arguments, progress_token, cancellation_context
            )
        elif name == "certify_output":
            return self._call_certify_output(
                req_id, arguments, progress_token, cancellation_context
            )
        elif name == "safe_execute":
            return self._call_safe_execute(
                req_id, arguments, progress_token, cancellation_context
            )
        elif name == "ask_agent":
            return self._call_ask_agent(
                req_id, arguments, progress_token, cancellation_context
            )
        elif name == "a2a_validate":
            return self._call_a2a_validate(req_id, arguments)
        elif name == "a2a_negotiate":
            return self._call_a2a_negotiate(req_id, arguments)
        else:
            return self._error(req_id, -32602, f"Unknown extended tool: {name}")
    except (AttributeError, ImportError, LookupError, OSError, RuntimeError, TypeError, ValueError):
        _LOG.exception("Tool call failed: %s", name)
        return self._result(
            req_id,
            {
                "content": [
                    {
                        "type": "text",
                        "text": "Tool execution failed. Check server logs for details.",
                    }
                ],
                "isError": True,
            },
        )

