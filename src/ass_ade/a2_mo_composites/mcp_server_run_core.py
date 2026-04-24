"""Tier a2 — assimilated method 'MCPServer.run'

Assimilated from: server.py:702-737
"""

from __future__ import annotations


# --- assimilated symbol ---
def run(self) -> None:
    """Run the stdio JSON-RPC loop. Reads from stdin, writes to stdout.

    Dispatches tool calls to a thread pool to keep stdin responsive during
    long-running operations (e.g., agent loops, Nexus API calls).
    """
    for line in sys.stdin:
        raw_bytes = len(line.encode("utf-8", errors="replace"))
        if raw_bytes > _MAX_LINE_BYTES:
            self._write(
                {
                    "jsonrpc": "2.0",
                    "id": None,
                    "error": {"code": -32700, "message": "Request too large"},
                }
            )
            continue
        line = line.strip()
        if not line:
            continue

        try:
            request = json.loads(line)
        except json.JSONDecodeError:
            self._write_error(None, -32700, "Parse error")
            continue

        # Dispatch to thread pool. The worker will call _handle_sync() and write the response.
        # This keeps stdin responsive for new requests and cancellations.
        req_id = request.get("id")
        future = self._executor.submit(self._handle_worker, request)

        # Track the future for cancellation support
        if req_id is not None:
            with self._lock:
                self._futures[req_id] = future

