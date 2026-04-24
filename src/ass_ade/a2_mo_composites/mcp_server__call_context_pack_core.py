"""Tier a2 — assimilated method 'MCPServer._call_context_pack'

Assimilated from: server.py:1249-1291
"""

from __future__ import annotations


# --- assimilated symbol ---
def _call_context_pack(
    self,
    req_id: Any,
    args: dict[str, Any],
    token: Any = None,
    cancellation_context: CancellationContext | None = None,
) -> dict[str, Any]:
    task_description = args.get("task_description", "")
    if not task_description:
        return self._error(req_id, -32602, "task_description is required")

    file_paths = args.get("file_paths")
    source_urls = args.get("source_urls") or []
    if file_paths is not None and not isinstance(file_paths, list):
        return self._error(req_id, -32602, "file_paths must be an array")
    if not isinstance(source_urls, list):
        return self._error(req_id, -32602, "source_urls must be an array")

    self._emit_progress(token, 0.0, message="Building context packet...")

    # Cancellation checkpoint
    if cancellation_context and cancellation_context.check():
        return self._error(req_id, -32800, "Request cancelled")

    from ass_ade.context_memory import build_context_packet

    packet = build_context_packet(
        task_description=task_description,
        working_dir=self._working_dir,
        file_paths=[str(path) for path in file_paths] if file_paths else None,
        source_urls=[str(url) for url in source_urls],
        max_files=int(args.get("max_files", 12)),
        max_bytes_per_file=int(args.get("max_bytes_per_file", 4000)),
    )
    self._emit_progress(token, 1.0, message="Context packet ready.")
    text = json.dumps(packet.model_dump(), indent=2)
    return self._result(
        req_id,
        {
            "content": [{"type": "text", "text": text}],
            "isError": packet.recon_verdict == "RECON_REQUIRED",
        },
    )

