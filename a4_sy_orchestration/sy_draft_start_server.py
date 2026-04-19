# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a4_sy_orchestration/sy_draft_start_server.py:7
# Component id: sy.source.a4_sy_orchestration.start_server
from __future__ import annotations

__version__ = "0.1.0"

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
