# Extracted from C:/!ass-ade/src/ass_ade/engine/tokens.py:127
# Component id: qk.source.ass_ade.estimate_tools_tokens
from __future__ import annotations

__version__ = "0.1.0"

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
