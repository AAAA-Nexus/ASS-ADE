# Extracted from C:/!ass-ade/.claude/worktrees/adoring-boyd-0e3a8f/src/ass_ade/nexus/client.py:381
# Component id: mo.source.ass_ade.internal_search
__version__ = "0.1.0"

    def internal_search(self, query: str, max_results: int = 10, session_token: str | None = None) -> list[dict]:
        """POST /internal/search — semantic search over the private knowledge base.

        Requires owner session token.
        """
        headers = {}
        if session_token:
            # Sanitize before inserting into an HTTP header (OWASP A03).
            headers["X-Owner-Token"] = sanitize_header_value(session_token.strip(), "session_token")
        response = self._client.post(
            "/internal/search",
            json={"query": query, "max_results": max_results},
            headers=headers,
        )
        raise_for_status(response.status_code, endpoint="/internal/search")
        return response.json()  # type: ignore[return-value]
