# Extracted from C:/!ass-ade/.claude/worktrees/adoring-boyd-0e3a8f/src/ass_ade/nexus/client.py:398
# Component id: mo.source.ass_ade.internal_search_chat
__version__ = "0.1.0"

    def internal_search_chat(self, query: str, session_token: str | None = None, **kwargs: Any) -> dict:
        """POST /internal/search/chat — RAG search + LLM answer.

        Requires owner session token.
        """
        headers = {}
        if session_token:
            # Sanitize before inserting into an HTTP header (OWASP A03).
            headers["X-Owner-Token"] = sanitize_header_value(session_token.strip(), "session_token")
        response = self._client.post(
            "/internal/search/chat",
            json={"query": query, **kwargs},
            headers=headers,
        )
        raise_for_status(response.status_code, endpoint="/internal/search/chat")
        return response.json()  # type: ignore[return-value]
