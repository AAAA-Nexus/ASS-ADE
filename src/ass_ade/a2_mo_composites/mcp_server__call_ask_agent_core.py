"""Tier a2 — assimilated method 'MCPServer._call_ask_agent'

Assimilated from: server.py:1488-1529
"""

from __future__ import annotations


# --- assimilated symbol ---
def _call_ask_agent(
    self,
    req_id: Any,
    args: dict[str, Any],
    token: Any = None,
    cancellation_context: CancellationContext | None = None,
) -> dict[str, Any]:
    task = args.get("task", "")
    if not task:
        return self._error(req_id, -32602, "task is required")
    model = args.get("model")
    self._emit_progress(token, 0.0, message="Starting agent loop...")

    # Cancellation checkpoint
    if cancellation_context and cancellation_context.check():
        return self._error(req_id, -32800, "Request cancelled")

    from ass_ade.agent.loop import AgentLoop
    from ass_ade.config import load_config
    from ass_ade.engine.router import build_provider

    cfg = load_config()
    provider = build_provider(cfg)
    try:
        loop = AgentLoop(
            provider=provider,
            registry=self._registry,
            working_dir=self._working_dir,
            model=model,
        )
        self._emit_progress(token, 0.3, message="Agent planning...")
        text = loop.step(task)
        text = text if text else "(no response)"
        return self._result(
            req_id,
            {
                "content": [{"type": "text", "text": text}],
                "isError": False,
            },
        )
    finally:
        provider.close()

