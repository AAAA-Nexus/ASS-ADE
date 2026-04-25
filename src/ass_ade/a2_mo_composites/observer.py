"""Tier a2 — event observer: collects events, writes JSONL logs, renders Rich CLI output."""
from __future__ import annotations

import json
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

VERBOSITY_VERBOSE = "verbose"
VERBOSITY_NORMAL = "normal"
VERBOSITY_QUIET = "quiet"

# Rich style and icon per event type (ASCII icons for Windows cp1252 compatibility)
_TYPE_STYLES: dict[str, tuple[str, str]] = {
    "thought":     ("dim white",  "~~ "),
    "tool_call":   ("cyan",       "-> "),
    "tool_result": ("green",      "<- "),
    "action":      ("yellow",     "** "),
    "intent":      ("bold blue",  ">> "),
    "error":       ("bold red",   "!! "),
    "decision":    ("magenta",    "?? "),
}

_QUIET_SHOW = frozenset({"error", "intent"})
_NORMAL_SHOW = frozenset({"tool_call", "intent", "error", "decision"})
_VERBOSE_SHOW = frozenset(_TYPE_STYLES)


@dataclass
class Observer:
    """Stateful event collector: renders to Rich console, persists to .ass-ade/logs/{date}.jsonl.

    verbosity:
        "verbose"  — show all event types
        "normal"   — show tool_call, intent, error, decision (default)
        "quiet"    — show only error and intent
    private:
        When True, message/result/args/context are stripped from log entries so
        sensitive content never lands on disk.
    narrator:
        Optional VoiceNarrator instance — when set, each recorded event is also
        forwarded to narrator.narrate_event() for TTS announcement.
    """

    working_dir: Path = field(default_factory=Path.cwd)
    verbosity: str = VERBOSITY_NORMAL
    private: bool = False
    narrator: Any = field(default=None, repr=False)  # VoiceNarrator | None

    _events: list[dict] = field(default_factory=list, init=False, repr=False)
    _console: Any = field(default=None, init=False, repr=False)
    _log_path: Path = field(init=False, repr=False)

    def __post_init__(self) -> None:
        try:
            from rich.console import Console
            self._console = Console()
        except ImportError:
            self._console = None

        log_dir = self.working_dir / ".ass-ade" / "logs"
        try:
            log_dir.mkdir(parents=True, exist_ok=True)
        except OSError:
            log_dir = Path.home() / ".ass-ade" / "logs"
            log_dir.mkdir(parents=True, exist_ok=True)

        date_str = datetime.now(timezone.utc).strftime("%Y-%m-%d")
        self._log_path = log_dir / f"{date_str}.jsonl"

    # ── Public API ─────────────────────────────────────────────────────────────

    def record(self, event: dict) -> None:
        """Accept an event dict, render it to the console, and append to the JSONL log."""
        self._events.append(event)
        self._render(event)
        self._persist(event)
        if self.narrator is not None:
            self.narrator.narrate_event(event)

    @property
    def event_count(self) -> int:
        return len(self._events)

    def events_of_type(self, type_: str) -> list[dict]:
        return [e for e in self._events if e.get("type") == type_]

    # ── Internals ──────────────────────────────────────────────────────────────

    def _render(self, event: dict) -> None:
        etype = event.get("type", "")
        if self.verbosity == VERBOSITY_VERBOSE:
            show = etype in _VERBOSE_SHOW
        elif self.verbosity == VERBOSITY_QUIET:
            show = etype in _QUIET_SHOW
        else:
            show = etype in _NORMAL_SHOW
        if not show:
            return

        style, icon = _TYPE_STYLES.get(etype, ("white", "  "))
        message = event.get("message", "")
        if self._console is not None:
            self._console.print(f"[{style}]{icon} {message}[/{style}]")
        else:
            print(f"{icon} {message}", flush=True)

    def _persist(self, event: dict) -> None:
        try:
            record = dict(event)
            if self.private:
                for key in ("message", "result", "args", "context"):
                    record.pop(key, None)
            with self._log_path.open("a", encoding="utf-8") as fh:
                fh.write(json.dumps(record, default=str) + "\n")
        except OSError:
            pass
