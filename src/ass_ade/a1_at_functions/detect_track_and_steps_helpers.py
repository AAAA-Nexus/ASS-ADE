"""Tier a1 — assimilated function 'detect_track_and_steps'

Assimilated from: rebuild/epiphany_cycle.py:11-44
"""

from __future__ import annotations


# --- assimilated symbol ---
def detect_track_and_steps(goal: str) -> tuple[str, list[str]]:
    """Classify goal into a track id and default step list (planner / MCP)."""
    normalized = goal.lower()

    if any(token in normalized for token in ("doc", "readme", "guide", "write", "document")):
        return "documentation", [
            "Audit the current documentation surface and note the missing reader outcomes.",
            "Outline the smallest document set that explains installation, usage, and limits.",
            "Draft the content with a clear separation between local behavior and remote behavior.",
            "Proofread for consistency with the public/private boundary before publishing.",
        ]

    if any(token in normalized for token in ("api", "mcp", "nexus", "endpoint", "integrate")):
        return "integration", [
            "Inspect the public contract first: OpenAPI, A2A manifest, and MCP manifest.",
            "Define the smallest typed adapter needed for the chosen integration path.",
            "Implement the adapter with graceful fallback and explicit error handling.",
            "Run a live or mocked smoke check against the public contract before shipping.",
        ]

    if any(token in normalized for token in ("test", "verify", "validate", "qa")):
        return "validation", [
            "Define the behaviors that must be proven correct before changing code.",
            "Add focused tests around the highest-risk paths first.",
            "Run validation locally and record any gaps that remain outside public scope.",
            "Update docs or examples if the verified behavior changes user expectations.",
        ]

    return "implementation", [
        "Define the smallest public-safe slice of the goal that creates real user value.",
        "Inspect the relevant code or contract surface before making any change.",
        "Implement the smallest end-to-end path with clean local fallback behavior.",
        "Validate the result with focused tests or smoke checks and tighten docs if needed.",
    ]

