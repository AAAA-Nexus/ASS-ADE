"""Tier a2 — assimilated method 'MCPServer._call_phase0_recon'

Assimilated from: server.py:1120-1164
"""

from __future__ import annotations


# --- assimilated symbol ---
def _call_phase0_recon(
    self,
    req_id: Any,
    args: dict[str, Any],
    token: Any = None,
    cancellation_context: CancellationContext | None = None,
) -> dict[str, Any]:
    task_description = args.get("task_description", "")
    if not task_description:
        return self._error(req_id, -32602, "task_description is required")

    provided_sources = args.get("provided_sources") or []
    if not isinstance(provided_sources, list):
        return self._error(req_id, -32602, "provided_sources must be an array")

    try:
        max_relevant_files = int(args.get("max_relevant_files", 20))
    except (TypeError, ValueError):
        return self._error(req_id, -32602, "max_relevant_files must be an integer")

    self._emit_progress(token, 0.0, message="Running Phase 0 codebase recon...")

    # Cancellation checkpoint
    if cancellation_context and cancellation_context.check():
        return self._error(req_id, -32800, "Request cancelled")

    from ass_ade.recon import phase0_recon

    result = phase0_recon(
        task_description=task_description,
        working_dir=self._working_dir,
        provided_sources=[str(source) for source in provided_sources],
        max_relevant_files=max_relevant_files,
    )
    self._emit_progress(
        token, 1.0, message=f"Phase 0 recon verdict: {result.verdict}"
    )
    text = json.dumps(result.model_dump(), indent=2)
    return self._result(
        req_id,
        {
            "content": [{"type": "text", "text": text}],
            "isError": result.verdict == "RECON_REQUIRED",
        },
    )

