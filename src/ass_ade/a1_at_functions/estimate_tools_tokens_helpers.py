"""Tier a1 — assimilated function 'estimate_tools_tokens'

Assimilated from: tokens.py:127-138
"""

from __future__ import annotations


# --- assimilated symbol ---
def estimate_tools_tokens(tools: list[ToolSchema]) -> int:
    """Estimate tokens consumed by tool schemas in the request."""
    if not tools:
        return 0
    # Each tool schema ~ serialized JSON
    total = 0
    for t in tools:
        total += estimate_tokens(t.name)
        total += estimate_tokens(t.description)
        total += estimate_tokens(json.dumps(t.parameters))
        total += 8  # schema framing overhead
    return total

