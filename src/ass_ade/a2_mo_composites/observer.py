"""Tier a2 — stateful observer: collects events, logs to JSONL, renders CLI output."""
from __future__ import annotations

import json
import sys
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

_STYLE_MAP: dict[str, str] = {
    "thought":     "dim cyan",
    "tool_call":   "bold yellow",
    "tool_result": "dim white",
    "action":      "bold blue",
    "intent":      "bold magenta",
    "error":       "bold red",
    "decision":    "bold green",
}


class Observer:
    """Session-scoped observability collector.

    Collects all events for a session, appends each to a JSONL log in real-time,
    and renders colour-coded output to stderr.

    Modes (set at construction):
      default  — render to stderr AND log to disk
      quiet    — log to disk only (private_mode=True, no_log=False)
      private  — neither render nor log (private_mode=True, no_log=True)
    """

    def __init__(
        self,
        *,
        log_dir: Path | None = None,
        session_id: str | None = None,
        private_mode: bool = False,
        no_log: bool = False,
    ) -> None:
        self.session_id = session_id or uuid.uuid4().hex[:8]
        self.private_mode = private_mode
        self._no_log = no_log
        self._events: list[dict[str, Any]] = []

        if not no_log:
            date_str = datetime.now(timezone.utc).strftime("%Y-%m-%d")
            self._log_dir = (log_dir or Path(".ass-ade") / "logs").resolve()
            self._log_dir.mkdir(parents=True, exist_ok=True)
            self._log_path: Path | None = (
                self._log_dir / f"{date_str}_{self.session_id}.jsonl"
            )
        else:
            self._log_path = None

    # ── Public API ─────────────────────────────────────────────────────────────

    def collect(self, event: dict[str, Any]) -> None:
        """Record event, append to JSONL log, and optionally render to terminal."""
        self._events.append(event)
        if not self._no_log:
            self._append_log(event)
        if not self.private_mode:
            self.render_cli(event)

    def render_cli(self, event: dict[str, Any]) -> None:
        """Print a colour-coded event line to stderr."""
        kind = event.get("type", "")
        msg = event.get("message", "")
        try:
            from rich.console import Console
            style = _STYLE_MAP.get(kind, "dim")
            Console(stderr=True, highlight=False).print(f"[{style}]{msg}[/{style}]")
        except ImportError:
            print(msg, flush=True, file=sys.stderr)

    def to_agui_event(self, event: dict[str, Any]) -> dict[str, Any]:
        """Convert an internal event to an AG-UI compatible payload."""
        return {
            "kind": event.get("type"),
            "text": event.get("message"),
            "ts": event.get("timestamp"),
            "data": event.get("data", {}),
            "session_id": self.session_id,
        }

    @property
    def events(self) -> list[dict[str, Any]]:
        return list(self._events)

    # ── Internal ───────────────────────────────────────────────────────────────

    def _append_log(self, event: dict[str, Any]) -> None:
        if self._log_path is None:
            return
        try:
            with self._log_path.open("a", encoding="utf-8") as f:
                f.write(json.dumps(event, default=str) + "\n")
        except Exception:
            pass
