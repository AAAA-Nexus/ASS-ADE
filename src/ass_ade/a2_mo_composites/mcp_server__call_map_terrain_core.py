"""Tier a2 — assimilated method 'MCPServer._call_map_terrain'

Assimilated from: server.py:1060-1118
"""

from __future__ import annotations


# --- assimilated symbol ---
def _call_map_terrain(
    self,
    req_id: Any,
    args: dict[str, Any],
    token: Any = None,
    cancellation_context: CancellationContext | None = None,
) -> dict[str, Any]:
    task_description = args.get("task_description", "")
    required = args.get("required_capabilities") or {}
    if not task_description:
        return self._error(req_id, -32602, "task_description is required")
    if not isinstance(required, dict):
        return self._error(
            req_id, -32602, "required_capabilities must be an object"
        )

    self._emit_progress(token, 0.0, message="Mapping required capabilities...")

    # Cancellation checkpoint
    if cancellation_context and cancellation_context.check():
        return self._error(req_id, -32800, "Request cancelled")

    hosted_tools: list[str] = []
    try:
        client = self._get_nexus_client()
        with client:
            manifest = client.get_mcp_manifest()
        hosted_tools = [tool.name or "" for tool in manifest.tools]
    except (ImportError, OSError, RuntimeError, TypeError, ValueError):
        hosted_tools = []

    self._emit_progress(
        token, 0.5, message="Checking local assets and hosted MCP tools..."
    )
    from ass_ade.map_terrain import map_terrain

    result = map_terrain(
        task_description=task_description,
        required_capabilities=required,
        agent_id=args.get("agent_id", "ass-ade-local"),
        max_development_budget_usdc=float(
            args.get("max_development_budget_usdc", 1.0)
        ),
        auto_invent_if_missing=bool(args.get("auto_invent_if_missing", False)),
        invention_constraints=args.get("invention_constraints") or {},
        working_dir=self._working_dir,
        hosted_tools=hosted_tools,
    )
    self._emit_progress(
        token, 1.0, message=f"MAP = TERRAIN verdict: {result.verdict}"
    )
    text = json.dumps(result.model_dump(), indent=2)
    return self._result(
        req_id,
        {
            "content": [{"type": "text", "text": text}],
            "isError": result.verdict == "HALT_AND_INVENT",
        },
    )

