"""Input validation for CLI-facing values before they hit the network.

Every validator returns the cleaned value or raises ``ValueError``
with a human-readable message.

Security guarantees
-------------------
``sanitize_header_value`` — blocks HTTP header injection (OWASP A03).
  CR (\\r), LF (\\n), and NUL in a header value allow request splitting.

``safe_path_segment`` — blocks path-traversal in URL-interpolated IDs
  (OWASP A01).  Only alphanumeric, dash, underscore, and dot are allowed.

``validate_api_key`` — prevents control characters in Bearer / X-API-Key
  headers that could split or poison the outgoing HTTP request.
"""

from __future__ import annotations

import ipaddress
import re
import socket as _socket
from urllib.parse import urlparse

_PRIVATE_NETS = [
    ipaddress.ip_network("127.0.0.0/8"),
    ipaddress.ip_network("10.0.0.0/8"),
    ipaddress.ip_network("172.16.0.0/12"),
    ipaddress.ip_network("192.168.0.0/16"),
    ipaddress.ip_network("169.254.0.0/16"),
    ipaddress.ip_network("::1/128"),
    ipaddress.ip_network("fc00::/7"),
]


def _is_private_host(hostname: str) -> bool:
    if not hostname:
        return True

    # Fast path for literal IPv4/IPv6 addresses.
    try:
        addr = ipaddress.ip_address(hostname)
        return any(addr in net for net in _PRIVATE_NETS)
    except ValueError:
        pass

    try:
        infos = _socket.getaddrinfo(hostname, None)
    except OSError:
        # DNS failures should not crash validation; fail closed for SSRF safety.
        return True

    for info in infos:
        sockaddr = info[4]
        if not sockaddr:
            continue
        ip_text = sockaddr[0]
        try:
            addr = ipaddress.ip_address(ip_text)
        except ValueError:
            continue
        if any(addr in net for net in _PRIVATE_NETS):
            return True
    return False


# Safe characters: alphanumeric, dash, underscore, dot, colon
_SAFE_ID_RE = re.compile(r"^[\w.\-:]{1,256}$")

# Safe URL path segment: same character set without colon (not valid in paths)
_SAFE_PATH_SEGMENT_RE = re.compile(r"^[\w.\-]{1,256}$")

# Characters that must never appear inside an HTTP header value
_HEADER_INJECTION_RE = re.compile(r"[\r\n\x00-\x08\x0b\x0c\x0e-\x1f\x7f]")

MAX_PROMPT_BYTES = 32_768  # 32 KB
MAX_USDC = 1_000_000.0


def validate_agent_id(value: str) -> str:
    """Non-empty, max 256 chars, safe characters only."""
    value = value.strip()
    if not value:
        raise ValueError("Agent ID must not be empty.")
    if len(value) > 256:
        raise ValueError(f"Agent ID exceeds 256 characters (got {len(value)}).")
    if not _SAFE_ID_RE.match(value):
        raise ValueError(
            "Agent ID contains invalid characters. "
            "Allowed: alphanumeric, dash, underscore, dot, colon."
        )
    return value


def validate_prompt(value: str) -> str:
    """Non-empty, max 32 KB, strip control characters."""
    if not value or not value.strip():
        raise ValueError("Prompt must not be empty.")
    # Strip control chars except newline and tab
    cleaned = re.sub(r"[\x00-\x08\x0b\x0c\x0e-\x1f\x7f]", "", value)
    if len(cleaned.encode("utf-8")) > MAX_PROMPT_BYTES:
        raise ValueError(f"Prompt exceeds {MAX_PROMPT_BYTES:,} bytes.")
    return cleaned


def validate_usdc_amount(value: float) -> float:
    """Positive, max 1,000,000 USDC."""
    if value <= 0:
        raise ValueError("USDC amount must be positive.")
    if value > MAX_USDC:
        raise ValueError(f"USDC amount exceeds maximum ({MAX_USDC:,.0f}).")
    return value


def validate_session_id(value: str) -> str:
    """Non-empty, max 256 chars."""
    value = value.strip()
    if not value:
        raise ValueError("Session ID must not be empty.")
    if len(value) > 256:
        raise ValueError(f"Session ID exceeds 256 characters (got {len(value)}).")
    return value


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


def validate_https_public_url(value: str, field_name: str = "URL") -> str:
    """Require an HTTPS URL that resolves to a public, non-loopback host."""
    value = validate_url(value)
    parsed = urlparse(value)
    if parsed.scheme != "https":
        raise ValueError(f"{field_name} must use https scheme (got '{parsed.scheme}').")
    return value


def sanitize_header_value(value: str, field_name: str = "header value") -> str:
    """Strip whitespace and reject any HTTP header-injection characters.

    CR (``\\r``), LF (``\\n``), and NUL (``\\x00``) in an HTTP header value
    allow request-splitting / CRLF injection attacks (OWASP A03).
    Raises ``ValueError`` if any such character is present after stripping.
    """
    value = value.strip()
    if _HEADER_INJECTION_RE.search(value):
        raise ValueError(
            f"{field_name} contains disallowed control characters "
            "(CR, LF, or other control characters are not permitted in "
            "HTTP header values — potential header injection)."
        )
    return value


def validate_api_key(value: str) -> str:
    """Non-empty, max 512 chars, no header-injection characters.

    Applied to any credential that ends up in an ``Authorization`` or
    ``X-API-Key`` HTTP header.
    """
    value = value.strip()
    if not value:
        raise ValueError("API key must not be empty.")
    if len(value) > 512:
        raise ValueError(f"API key exceeds 512 characters (got {len(value)}).")
    return sanitize_header_value(value, "API key")


def safe_path_segment(value: str, name: str = "ID") -> str:
    """Validate that *value* is safe to interpolate into a URL path segment.

    Rejects empty values, values exceeding 256 characters, and any character
    that is not alphanumeric, dash, underscore, or dot.  This prevents path
    traversal (``../``) and injection via IDs passed to f-string URL templates
    (OWASP A01).
    """
    value = value.strip()
    if not value:
        raise ValueError(f"{name} must not be empty.")
    if len(value) > 256:
        raise ValueError(f"{name} exceeds 256 characters (got {len(value)}).")
    if not _SAFE_PATH_SEGMENT_RE.match(value):
        raise ValueError(
            f"{name} contains invalid characters for a URL path segment. "
            "Only alphanumeric characters, dash, underscore, and dot are allowed."
        )
    return value
