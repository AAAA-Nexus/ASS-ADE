from __future__ import annotations

from ass_ade.engine.rebuild.epiphany_cycle import (
    EPIPHANY_PHASE_STEPS,
    detect_track_and_steps,
)


def _detect_track(goal: str) -> tuple[str, list[str]]:
    return detect_track_and_steps(goal)


def resolve_plan_track(goal: str) -> tuple[str, list[str]]:
    """Return ``(track_id, base_steps)`` for orchestration (MCP, CLI)."""
    return detect_track_and_steps(goal)


def draft_plan(goal: str, max_steps: int = 5) -> list[str]:
    if not goal.strip():
        raise ValueError("Goal must not be empty.")

    _, steps = _detect_track(goal)
    intro = f"Define success criteria for: {goal.strip()}"
    plan = [intro, *steps]
    return plan[:max_steps]


def draft_epiphany_breakthrough_plan(goal: str, max_steps: int = 12) -> list[str]:
    """Governance-style envelope: epiphany phases then track-specific steps."""
    if not goal.strip():
        raise ValueError("Goal must not be empty.")

    _, base = _detect_track(goal)
    intro = f"Goal: {goal.strip()}"
    merged = [intro, *EPIPHANY_PHASE_STEPS, "--- Track-specific steps ---", *base]
    return merged[:max_steps]


def render_markdown(goal: str, steps: list[str]) -> str:
    lines = ["# Draft Plan", "", f"Goal: {goal}", ""]
    lines.extend(f"{index}. {step}" for index, step in enumerate(steps, start=1))
    return "\n".join(lines)
