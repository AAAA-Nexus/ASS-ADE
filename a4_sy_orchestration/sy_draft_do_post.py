# Extracted from C:/!ass-ade/.claude/worktrees/adoring-boyd-0e3a8f/src/ass_ade/mcp/mock_server.py:59
# Component id: sy.source.ass_ade.do_post
__version__ = "0.1.0"

    def do_POST(self) -> None:  # noqa: N802
        try:
            raw_length = int(self.headers.get("Content-Length", "0"))
        except ValueError:
            self._send_json(400, {"error": "invalid Content-Length"})
            return
        if raw_length > _MAX_BODY_BYTES:
            # Drain the announced body so the connection can be closed cleanly.
            remaining = raw_length
            while remaining > 0:
                chunk = self.rfile.read(min(65536, remaining))
                if not chunk:
                    break
                remaining -= len(chunk)
            self._send_json(413, {"error": "request entity too large"})
            return
        length = raw_length
        body: Any = {}
        if length:
            try:
                body = json.loads(self.rfile.read(length).decode("utf-8"))
            except Exception:
                self._send_json(400, {"error": "invalid JSON"})
                return
        # Echo back the payload with the matched path
        self._send_json(200, {"echo": body, "path": self.path})
