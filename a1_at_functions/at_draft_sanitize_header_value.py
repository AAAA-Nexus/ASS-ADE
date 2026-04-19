# Extracted from C:/!ass-ade/src/ass_ade/nexus/validation.py:150
# Component id: at.source.ass_ade.sanitize_header_value
from __future__ import annotations

__version__ = "0.1.0"

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
