# Extracted from C:/!ass-ade/src/ass_ade/a2a/__init__.py:188
# Component id: at.source.ass_ade.fetch_agent_card
from __future__ import annotations

__version__ = "0.1.0"

def fetch_agent_card(url: str, *, timeout: float = 10.0) -> ValidationReport:
    """Fetch and validate an agent card from a URL.

    If the URL doesn't end with /.well-known/agent.json, it is appended.

    SSRF validation is performed immediately before the network request to
    minimize the DNS rebinding TOCTOU window (time-of-check to time-of-use).
    """
    if not url.endswith("/.well-known/agent.json"):
        url = url.rstrip("/") + "/.well-known/agent.json"

    # Early format check only (hostname, scheme)
    parsed = urlparse(url)
    if parsed.scheme != "https":
        return ValidationReport(
            valid=False,
            issues=[ValidationIssue("error", "_fetch", "Only HTTPS URLs are permitted for agent card fetching.")],
        )
    if not parsed.hostname:
        return ValidationReport(
            valid=False,
            issues=[ValidationIssue("error", "_fetch", "URL has no hostname.")],
        )

    try:
        # CRITICAL: Re-validate immediately before the actual network request
        # to minimize DNS rebinding TOCTOU attacks. We check that:
        # 1. The hostname resolves
        # 2. All resolved IPs are in public ranges (not private/loopback)
        ssrf_err = _check_ssrf(url)
        if ssrf_err:
            return ValidationReport(
                valid=False,
                issues=[ValidationIssue("error", "_fetch", ssrf_err)],
            )

        resp = httpx.get(url, timeout=timeout, follow_redirects=False)
        resp.raise_for_status()
        data = resp.json()
    except httpx.HTTPStatusError as exc:
        return ValidationReport(
            valid=False,
            issues=[ValidationIssue("error", "_fetch", f"HTTP {exc.response.status_code}: {url}")],
        )
    except httpx.RequestError as exc:
        return ValidationReport(
            valid=False,
            issues=[ValidationIssue("error", "_fetch", f"Network error: {exc}")],
        )
    except json.JSONDecodeError:
        return ValidationReport(
            valid=False,
            issues=[ValidationIssue("error", "_fetch", "Response is not valid JSON")],
        )

    return validate_agent_card(data)
