# Extracted from C:/!ass-ade/src/ass_ade/nexus/validation.py:125
# Component id: at.source.ass_ade.validate_url
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
