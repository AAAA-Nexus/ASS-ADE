"""Tier a1 — pure helpers for observable event emission."""
from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from typing import Any


class EventKind(str, Enum):
    THOUGHT = "thought"
    TOOL_CALL = "tool_call"
    TOOL_RESULT = "tool_result"
    ACTION = "action"
    INTENT = "intent"
    ERROR = "error"
    DECISION = "decision"


@dataclass(frozen=True)
class ObservableEvent:
    kind: EventKind
    payload: dict[str, Any]
    timestamp: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    session_id: str = ""

    def to_dict(self) -> dict[str, Any]:
        return {
            "kind": self.kind.value,
            "payload": self.payload,
            "timestamp": self.timestamp,
            "session_id": self.session_id,
        }


def emit_thought(content: str, session_id: str = "") -> ObservableEvent:
    """Emit a thought event — internal reasoning before acting."""
    return ObservableEvent(
        kind=EventKind.THOUGHT,
        payload={"content": content},
        session_id=session_id,
    )


def emit_tool_call(tool: str, args: dict[str, Any], session_id: str = "") -> ObservableEvent:
    """Emit a tool call event — before dispatching a CLI command or tool."""
    return ObservableEvent(
        kind=EventKind.TOOL_CALL,
        payload={"tool": tool, "args": args},
        session_id=session_id,
    )


def emit_tool_result(
    tool: str,
    result: Any,
    ok: bool = True,
    session_id: str = "",
) -> ObservableEvent:
    """Emit a tool result event — after a CLI command or tool completes."""
    return ObservableEvent(
        kind=EventKind.TOOL_RESULT,
        payload={"tool": tool, "result": result, "ok": ok},
        session_id=session_id,
    )


def emit_action(
    name: str,
    details: dict[str, Any] | None = None,
    session_id: str = "",
) -> ObservableEvent:
    """Emit an action event — a significant user-visible step in the pipeline."""
    return ObservableEvent(
        kind=EventKind.ACTION,
        payload={"name": name, **(details or {})},
        session_id=session_id,
    )


def emit_intent(
    intent: str,
    confidence: float = 1.0,
    source: str = "heuristic",
    session_id: str = "",
) -> ObservableEvent:
    """Emit an intent classification event — how the user input was interpreted."""
    return ObservableEvent(
        kind=EventKind.INTENT,
        payload={"intent": intent, "confidence": confidence, "source": source},
        session_id=session_id,
    )


def emit_error(
    message: str,
    context: dict[str, Any] | None = None,
    session_id: str = "",
) -> ObservableEvent:
    """Emit an error event — something failed or was unexpected."""
    return ObservableEvent(
        kind=EventKind.ERROR,
        payload={"message": message, **(context or {})},
        session_id=session_id,
    )


def emit_decision(
    choice: str,
    reason: str,
    alternatives: list[str] | None = None,
    session_id: str = "",
) -> ObservableEvent:
    """Emit a decision event — a deliberate choice between alternatives."""
    return ObservableEvent(
        kind=EventKind.DECISION,
        payload={"choice": choice, "reason": reason, "alternatives": alternatives or []},
        session_id=session_id,
    )
