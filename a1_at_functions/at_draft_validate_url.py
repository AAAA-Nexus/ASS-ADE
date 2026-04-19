# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a1_at_functions/at_draft_validate_url.py:7
# Component id: at.source.a1_at_functions.validate_url
from __future__ import annotations

__version__ = "0.1.0"

def validate_url(value: str) -> str:
    """Must be a valid HTTP(S) URL with no control characters in the host."""
    value = value.strip()
    parsed = urlparse(value)
    if parsed.scheme not in ("http", "https"):
        raise ValueError(f"URL must use http or https scheme (got '{parsed.scheme}').")
    if not parsed.netloc:
        raise ValueError("URL must have a valid host.")
    if _HEADER_INJECTION_RE.search(parsed.netloc):
        raise ValueError("URL host contains disallowed control characters.")
    hostname = parsed.hostname or ""
    if _is_private_host(hostname):
        raise ValueError(f"URL targets private/loopback address: {hostname}")
    return value
