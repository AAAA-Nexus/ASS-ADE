# Extracted from C:/!ass-ade/.claude/worktrees/adoring-boyd-0e3a8f/src/ass_ade/nexus/validation.py:181
# Component id: at.source.ass_ade.safe_path_segment
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
