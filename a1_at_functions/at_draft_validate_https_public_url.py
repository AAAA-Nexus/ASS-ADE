# Extracted from C:/!ass-ade/.claude/worktrees/adoring-boyd-0e3a8f/src/ass_ade/nexus/validation.py:141
# Component id: at.source.ass_ade.validate_https_public_url
__version__ = "0.1.0"

def validate_https_public_url(value: str, field_name: str = "URL") -> str:
    """Require an HTTPS URL that resolves to a public, non-loopback host."""
    value = validate_url(value)
    parsed = urlparse(value)
    if parsed.scheme != "https":
        raise ValueError(f"{field_name} must use https scheme (got '{parsed.scheme}').")
    return value
