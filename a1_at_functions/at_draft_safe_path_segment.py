# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a1_at_functions/at_draft_safe_path_segment.py:7
# Component id: at.source.a1_at_functions.safe_path_segment
from __future__ import annotations

__version__ = "0.1.0"

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
