"""Tier a1 — pure event-payload constructors for the observability layer."""
from __future__ import annotations

from datetime import datetime, timezone
from typing import Any


def _event(type_: str, message: str, **extra: Any) -> dict:
    return {
        "type": type_,
        "message": message,
        "timestamp": datetime.now(timezone.utc).isoformat(),
        **extra,
    }


def emit_thought(message: str, **extra: Any) -> dict:
    """Internal reasoning or pre-call annotation."""
    return _event("thought", message, **extra)


def emit_tool_call(tool: str, args: dict | None = None, **extra: Any) -> dict:
    """Signal that a tool (subprocess, LLM, etc.) is about to be called."""
    return _event("tool_call", f"→ {tool}", tool=tool, args=args or {}, **extra)


def emit_tool_result(tool: str, result: Any, **extra: Any) -> dict:
    """Signal the result returned by a tool."""
    summary = str(result)[:200] if result is not None else ""
    return _event("tool_result", f"← {tool}: {summary}", tool=tool, result=result, **extra)


def emit_action(action: str, details: Any = None, **extra: Any) -> dict:
    """A concrete action taken (file write, command run, etc.)."""
    msg = action if details is None else f"{action}: {details}"
    return _event("action", msg, action=action, details=details, **extra)


def emit_intent(intent: str, path: str = "", **extra: Any) -> dict:
    """Intent derived from user input, ready for dispatch."""
    msg = f"intent={intent}" + (f"  path={path}" if path else "")
    return _event("intent", msg, intent=intent, path=path, **extra)


def emit_error(error: str, context: Any = None, **extra: Any) -> dict:
    """An error or unexpected failure condition."""
    return _event("error", error, context=context, **extra)


def emit_decision(decision: str, reason: str = "", **extra: Any) -> dict:
    """A branching decision point with optional justification."""
    msg = decision if not reason else f"{decision} — {reason}"
    return _event("decision", msg, decision=decision, reason=reason, **extra)
