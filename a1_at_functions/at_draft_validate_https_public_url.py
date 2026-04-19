# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a1_at_functions/at_draft_validate_https_public_url.py:7
# Component id: at.source.a1_at_functions.validate_https_public_url
from __future__ import annotations

__version__ = "0.1.0"

def validate_https_public_url(value: str, field_name: str = "URL") -> str:
    """Require an HTTPS URL that resolves to a public, non-loopback host."""
    value = validate_url(value)
    parsed = urlparse(value)
    if parsed.scheme != "https":
        raise ValueError(f"{field_name} must use https scheme (got '{parsed.scheme}').")
    return value
