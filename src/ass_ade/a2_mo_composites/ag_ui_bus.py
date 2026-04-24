"""Tier a2 — AG-UI event bus: pub/sub for agent→frontend streaming.

Implements a subset of the AG-UI protocol (https://docs.ag-ui.com/) as an
in-process event bus. The FastAPI server (a3) subscribes to this bus and
forwards events to frontend clients over Server-Sent Events. The interpreter
publishes events as it runs turns, executes skills, and mutates state.

Event types follow AG-UI naming for interoperability:
  RUN_STARTED / RUN_FINISHED / RUN_ERROR
  TEXT_MESSAGE_START / TEXT_MESSAGE_CONTENT / TEXT_MESSAGE_END
  TOOL_CALL_START / TOOL_CALL_ARGS / TOOL_CALL_RESULT / TOOL_CALL_END
  STATE_SNAPSHOT / STATE_DELTA

Plus one ASS-ADE extension for typed widget cards (A2UI-style):
  WIDGET_CARD — carries {kind, payload}, e.g. kind="scout_report"
"""

from __future__ import annotations

import asyncio
import json
import time
import uuid
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, AsyncIterator


class AGUIEventType(str, Enum):
    RUN_STARTED = "RUN_STARTED"
    RUN_FINISHED = "RUN_FINISHED"
    RUN_ERROR = "RUN_ERROR"
    TEXT_MESSAGE_START = "TEXT_MESSAGE_START"
    TEXT_MESSAGE_CONTENT = "TEXT_MESSAGE_CONTENT"
    TEXT_MESSAGE_END = "TEXT_MESSAGE_END"
    TOOL_CALL_START = "TOOL_CALL_START"
    TOOL_CALL_ARGS = "TOOL_CALL_ARGS"
    TOOL_CALL_RESULT = "TOOL_CALL_RESULT"
    TOOL_CALL_END = "TOOL_CALL_END"
    STATE_SNAPSHOT = "STATE_SNAPSHOT"
    STATE_DELTA = "STATE_DELTA"
    WIDGET_CARD = "WIDGET_CARD"


@dataclass
class AGUIEvent:
    """Single AG-UI event — JSON-serializable, SSE-ready."""
    type: AGUIEventType
    data: dict = field(default_factory=dict)
    run_id: str = ""
    timestamp: float = field(default_factory=time.time)

    def to_dict(self) -> dict:
        return {
            "type": self.type.value,
            "data": self.data,
            "runId": self.run_id,
            "ts": self.timestamp,
        }

    def to_sse(self) -> str:
        return f"data: {json.dumps(self.to_dict(), default=str)}\n\n"


class AGUIBus:
    """In-process event bus. Multiple SSE clients can subscribe concurrently.

    Keeps a ring-buffer of recent events so late subscribers can optionally
    replay (useful for a dashboard reloading mid-session).
    """

    def __init__(self, buffer_size: int = 500) -> None:
        self._subscribers: list[asyncio.Queue] = []
        self._history: list[AGUIEvent] = []
        self._buffer_size = buffer_size
        self._state: dict[str, Any] = {}

    # ── Publishing ─────────────────────────────────────────────────────────────

    def publish(self, event: AGUIEvent) -> None:
        self._history.append(event)
        if len(self._history) > self._buffer_size:
            self._history = self._history[-self._buffer_size:]
        for q in list(self._subscribers):
            try:
                q.put_nowait(event)
            except asyncio.QueueFull:
                pass

    def emit(self, type_: AGUIEventType, data: dict | None = None, run_id: str = "") -> AGUIEvent:
        """Convenience: construct + publish in one call. Returns the event."""
        ev = AGUIEvent(type=type_, data=data or {}, run_id=run_id)
        self.publish(ev)
        return ev

    def emit_widget(self, kind: str, payload: dict, run_id: str = "") -> AGUIEvent:
        """Emit a typed widget card (A2UI-style generative UI slot)."""
        return self.emit(
            AGUIEventType.WIDGET_CARD,
            {"kind": kind, "payload": payload},
            run_id=run_id,
        )

    # ── State management ───────────────────────────────────────────────────────

    def set_state(self, path: str, value: Any) -> None:
        """Set a dotted-path state value and emit a STATE_DELTA."""
        keys = [k for k in path.split(".") if k]
        if not keys:
            return
        node = self._state
        for k in keys[:-1]:
            next_node = node.get(k)
            if not isinstance(next_node, dict):
                next_node = {}
                node[k] = next_node
            node = next_node
        node[keys[-1]] = value
        self.emit(AGUIEventType.STATE_DELTA, {"path": path, "value": value})

    def snapshot(self) -> dict:
        return dict(self._state)

    def emit_snapshot(self) -> AGUIEvent:
        return self.emit(AGUIEventType.STATE_SNAPSHOT, {"state": self.snapshot()})

    # ── Subscription ───────────────────────────────────────────────────────────

    async def subscribe(self, replay: int = 0) -> AsyncIterator[AGUIEvent]:
        queue: asyncio.Queue = asyncio.Queue(maxsize=1000)
        self._subscribers.append(queue)
        try:
            if replay:
                for event in self._history[-replay:]:
                    yield event
            while True:
                event = await queue.get()
                yield event
        finally:
            if queue in self._subscribers:
                self._subscribers.remove(queue)

    # ── Introspection ──────────────────────────────────────────────────────────

    def history(self, limit: int = 50) -> list[dict]:
        return [e.to_dict() for e in self._history[-limit:]]

    def new_run_id(self) -> str:
        return f"run-{uuid.uuid4().hex[:12]}"

    def subscriber_count(self) -> int:
        return len(self._subscribers)

    def clear(self) -> None:
        self._history.clear()
        self._state.clear()


# Module-level singleton — the interpreter publishes here, FastAPI forwards.
_BUS: AGUIBus | None = None


def get_bus() -> AGUIBus:
    global _BUS
    if _BUS is None:
        _BUS = AGUIBus()
    return _BUS


def reset_bus() -> None:
    """Reset the singleton (for tests)."""
    global _BUS
    _BUS = None
