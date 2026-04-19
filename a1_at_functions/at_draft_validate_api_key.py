# Extracted from C:/!ass-ade/.claude/worktrees/adoring-boyd-0e3a8f/src/ass_ade/nexus/validation.py:167
# Component id: at.source.ass_ade.validate_api_key
__version__ = "0.1.0"

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
