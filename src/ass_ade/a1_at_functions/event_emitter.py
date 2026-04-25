"""Tier a1 — pure event-formatting functions for the observability layer."""
from __future__ import annotations

import json
from datetime import datetime, timezone
from typing import Any


def _event(type_: str, message: str, data: dict[str, Any] | None = None) -> dict[str, Any]:
    return {
        "type": type_,
        "message": message,
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "data": data or {},
    }


def emit_thought(text: str) -> dict[str, Any]:
    """Format a thinking event: '🧠 Thinking: {text}'."""
    return _event("thought", f"🧠 Thinking: {text}", {"text": text})


def emit_tool_call(tool_name: str, args: dict[str, Any]) -> dict[str, Any]:
    """Format a tool invocation event: '🔧 Tool: {tool_name}({args})'."""
    args_str = json.dumps(args, default=str)[:200]
    return _event(
        "tool_call",
        f"🔧 Tool: {tool_name}({args_str})",
        {"tool": tool_name, "args": args},
    )


def emit_tool_result(tool_name: str, result_summary: str) -> dict[str, Any]:
    """Format a tool result event: '📄 Result: {summary}'."""
    return _event(
        "tool_result",
        f"📄 Result: {result_summary[:200]}",
        {"tool": tool_name, "summary": result_summary[:500]},
    )


def emit_action(text: str) -> dict[str, Any]:
    """Format an action event: '⚡ Action: {text}'."""
    return _event("action", f"⚡ Action: {text}", {"text": text})


def emit_intent(intent: str, confidence: float) -> dict[str, Any]:
    """Format an intent event: '🎯 Intent: {intent} ({confidence})'."""
    pct = f"{confidence:.0%}"
    return _event(
        "intent",
        f"🎯 Intent: {intent} ({pct})",
        {"intent": intent, "confidence": confidence},
    )


def emit_error(text: str) -> dict[str, Any]:
    """Format an error event: '❌ Error: {text}'."""
    return _event("error", f"❌ Error: {text}", {"text": text})


def emit_decision(text: str) -> dict[str, Any]:
    """Format a decision event: '✅ Decision: {text}'."""
    return _event("decision", f"✅ Decision: {text}", {"text": text})
