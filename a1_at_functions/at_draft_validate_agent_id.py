# Extracted from C:/!ass-ade/.claude/worktrees/beautiful-dubinsky-c2cb48/a1_at_functions/at_draft_validate_agent_id.py:5
# Component id: at.source.ass_ade.validate_agent_id
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
