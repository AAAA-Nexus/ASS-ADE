from __future__ import annotations


def _detect_track(goal: str) -> tuple[str, list[str]]:
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


def draft_plan(goal: str, max_steps: int = 5) -> list[str]:
    if not goal.strip():
        raise ValueError("Goal must not be empty.")

    _, steps = _detect_track(goal)
    intro = f"Define success criteria for: {goal.strip()}"
    plan = [intro, *steps]
    return plan[:max_steps]


def render_markdown(goal: str, steps: list[str]) -> str:
    lines = ["# Draft Plan", "", f"Goal: {goal}", ""]
    lines.extend(f"{index}. {step}" for index, step in enumerate(steps, start=1))
    return "\n".join(lines)

