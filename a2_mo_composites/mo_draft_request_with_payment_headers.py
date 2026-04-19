# Extracted from C:/!ass-ade/.claude/worktrees/adoring-boyd-0e3a8f/src/ass_ade/nexus/client.py:359
# Component id: mo.source.ass_ade.request_with_payment_headers
__version__ = "0.1.0"

    def request_with_payment_headers(
        self,
        path: str,
        body: dict | None = None,
        *,
        payment_headers: dict[str, str],
    ) -> httpx.Response:
        """POST to *path* with *payment_headers* merged in.

        Use this for the second leg of an x402 payment flow, where the
        payment proof headers (from the wallet) must accompany the actual request.
        """
        # Sanitize all header values before forwarding to prevent header injection
        # when this method is called with user-controlled payment proof headers (OWASP A03).
        safe_headers = {
            k: sanitize_header_value(str(v), f"payment_headers[{k!r}]")
            for k, v in payment_headers.items()
        }
        return self._client.post(path, json=body or {}, headers=safe_headers)
