"""Tier a1 — assimilated function 'start_server'

Assimilated from: mock_server.py:95-122
"""

from __future__ import annotations


# --- assimilated symbol ---
def start_server(
    port: int = 8787,
    *,
    manifest_path: Path | None = None,
    block: bool = True,
) -> HTTPServer | None:
    """Start the mock server.

    Returns the ``HTTPServer`` instance. When ``block=False`` the server
    runs in a daemon thread so it stops automatically when the process exits.
    """
    manifest = _DEFAULT_MANIFEST.copy()
    if manifest_path is not None and manifest_path.exists():
        try:
            manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        except Exception:
            pass  # fall back to default manifest

    handler_cls = build_handler(manifest)
    server = HTTPServer(("127.0.0.1", port), handler_cls)

    if not block:
        t = threading.Thread(target=server.serve_forever, daemon=True)
        t.start()
        return server

    server.serve_forever()
    return None

