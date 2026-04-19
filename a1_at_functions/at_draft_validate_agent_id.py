# Extracted from C:/!ass-ade/src/ass_ade/nexus/validation.py:80
# Component id: at.source.ass_ade.validate_agent_id
from __future__ import annotations

__version__ = "0.1.0"

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
