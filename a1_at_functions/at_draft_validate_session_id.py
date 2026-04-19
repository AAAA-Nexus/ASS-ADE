# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a1_at_functions/at_draft_validate_session_id.py:7
# Component id: at.source.a1_at_functions.validate_session_id
from __future__ import annotations

__version__ = "0.1.0"

def validate_session_id(value: str) -> str:
    """Non-empty, max 256 chars."""
    value = value.strip()
    if not value:
        raise ValueError("Session ID must not be empty.")
    if len(value) > 256:
        raise ValueError(f"Session ID exceeds 256 characters (got {len(value)}).")
    return value
