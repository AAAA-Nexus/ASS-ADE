"""Tier a2 — Observer: collects events, writes logs, renders Rich CLI output."""
from __future__ import annotations

import json
import os
import sys
from datetime import datetime, timezone
from pathlib import Path
from threading import Lock
from typing import Any

from ass_ade.a1_at_functions.event_emitter import EventKind, ObservableEvent

# ── Verbosity modes ───────────────────────────────────────────────────────────
# verbose (default ON): full event stream with colors
# quiet:  only errors and final results
# private: no output at all (used in tests / pipelines)

VERBOSE = "verbose"
QUIET = "quiet"
PRIVATE = "private"

_VERBOSITY_ENV = "ASS_ADE_VERBOSITY"
_LOG_DIR_ENV = "ASS_ADE_LOG_DIR"

# ── Rich color scheme ──────────────────────────────────────────────────────────
_KIND_STYLES: dict[EventKind, str] = {
    EventKind.THOUGHT:     "dim cyan",
    EventKind.TOOL_CALL:   "bold yellow",
    EventKind.TOOL_RESULT: "green",
    EventKind.ACTION:      "bold blue",
    EventKind.INTENT:      "bold magenta",
    EventKind.ERROR:       "bold red",
    EventKind.DECISION:    "bold white",
}

_KIND_PREFIX: dict[EventKind, str] = {
    EventKind.THOUGHT:     "💭",
    EventKind.TOOL_CALL:   "🔧",
    EventKind.TOOL_RESULT: "✅",
    EventKind.ACTION:      "⚡",
    EventKind.INTENT:      "🧠",
    EventKind.ERROR:       "❌",
    EventKind.DECISION:    "🎯",
}


class Observer:
    """Collects ObservableEvents, logs them to disk, and renders them to the CLI.

    Usage:
        obs = Observer.get()  # singleton per process
        obs.collect(emit_intent("recon", source="llm"))

    CLI flags inject verbosity:
        --verbose (default ON): full event stream
        --quiet:   suppress all except errors + final result
        --private: no output (logging only)
    """

    _instance: "Observer | None" = None
    _lock: Lock = Lock()

    def __init__(
        self,
        verbosity: str = VERBOSE,
        log_dir: Path | None = None,
        session_id: str = "",
    ) -> None:
        self.verbosity = verbosity
        self.session_id = session_id or datetime.now(timezone.utc).strftime("%Y%m%d-%H%M%S")
        self._events: list[ObservableEvent] = []
        self._log_dir = log_dir or self._default_log_dir()
        self._log_file: Path | None = None
        self._use_rich = self._detect_rich()
        self._console: Any = None
        if self._use_rich:
            try:
                from rich.console import Console
                self._console = Console(highlight=False)
            except Exception:
                self._use_rich = False

    # ── Singleton ─────────────────────────────────────────────────────────────

    @classmethod
    def get(
        cls,
        *,
        verbosity: str | None = None,
        log_dir: Path | None = None,
        session_id: str = "",
    ) -> "Observer":
        """Return the process-wide Observer, creating it on first call."""
        with cls._lock:
            if cls._instance is None:
                v = verbosity or os.environ.get(_VERBOSITY_ENV, VERBOSE)
                ld = log_dir
                if ld is None and os.environ.get(_LOG_DIR_ENV):
                    ld = Path(os.environ[_LOG_DIR_ENV])
                cls._instance = cls(verbosity=v, log_dir=ld, session_id=session_id)
            elif verbosity is not None:
                cls._instance.verbosity = verbosity
            return cls._instance

    @classmethod
    def reset(cls) -> None:
        """Reset the singleton — useful in tests."""
        with cls._lock:
            cls._instance = None

    # ── Verbosity helpers ─────────────────────────────────────────────────────

    def set_verbose(self) -> None:
        self.verbosity = VERBOSE

    def set_quiet(self) -> None:
        self.verbosity = QUIET

    def set_private(self) -> None:
        self.verbosity = PRIVATE

    # ── Core collect + render ──────────────────────────────────────────────────

    def collect(self, event: ObservableEvent) -> None:
        """Accept an event: store it, log to disk, print to CLI."""
        self._events.append(event)
        self._log_event(event)
        self._render(event)

    def _render(self, event: ObservableEvent) -> None:
        if self.verbosity == PRIVATE:
            return
        if self.verbosity == QUIET and event.kind != EventKind.ERROR:
            return

        prefix = _KIND_PREFIX.get(event.kind, "·")
        style = _KIND_STYLES.get(event.kind, "white")
        line = self._format_event(event, prefix)

        if self._use_rich and self._console:
            self._console.print(f"[{style}]{line}[/{style}]")
        else:
            print(line, file=sys.stderr if event.kind == EventKind.ERROR else sys.stdout,
                  flush=True)

    def _format_event(self, event: ObservableEvent, prefix: str) -> str:
        p = event.payload
        if event.kind == EventKind.INTENT:
            src = p.get("source", "heuristic")
            conf = p.get("confidence", 1.0)
            conf_str = f" ({conf:.0%})" if conf < 1.0 else ""
            return f"{prefix} intent={p['intent']}{conf_str} via {src}"
        if event.kind == EventKind.TOOL_CALL:
            args_preview = ", ".join(f"{k}={v!r}" for k, v in list(p.get("args", {}).items())[:3])
            return f"{prefix} {p['tool']}({args_preview})"
        if event.kind == EventKind.TOOL_RESULT:
            ok = "✓" if p.get("ok") else "✗"
            result_preview = str(p.get("result", ""))[:80].replace("\n", " ")
            return f"{prefix} {p['tool']} {ok} → {result_preview}"
        if event.kind == EventKind.THOUGHT:
            return f"{prefix} {p.get('content', '')[:120]}"
        if event.kind == EventKind.ACTION:
            details = {k: v for k, v in p.items() if k != "name"}
            detail_str = " | ".join(f"{k}={v}" for k, v in list(details.items())[:3])
            return f"{prefix} {p['name']}" + (f" — {detail_str}" if detail_str else "")
        if event.kind == EventKind.ERROR:
            return f"{prefix} {p.get('message', 'unknown error')}"
        if event.kind == EventKind.DECISION:
            alts = p.get("alternatives", [])
            alts_str = f" (vs {', '.join(alts[:2])})" if alts else ""
            return f"{prefix} chose={p['choice']}{alts_str} — {p.get('reason', '')[:80]}"
        return f"{prefix} {json.dumps(p)[:120]}"

    # ── Disk logging ───────────────────────────────────────────────────────────

    def _log_event(self, event: ObservableEvent) -> None:
        try:
            log_path = self._ensure_log_file()
            with log_path.open("a", encoding="utf-8") as fh:
                fh.write(json.dumps(event.to_dict()) + "\n")
        except OSError:
            pass

    def _ensure_log_file(self) -> Path:
        if self._log_file is None:
            self._log_dir.mkdir(parents=True, exist_ok=True)
            self._log_file = self._log_dir / f"session-{self.session_id}.jsonl"
        return self._log_file

    @staticmethod
    def _default_log_dir() -> Path:
        return Path.home() / ".ass-ade" / "logs"

    # ── Query API ──────────────────────────────────────────────────────────────

    def events(self, kind: EventKind | None = None) -> list[ObservableEvent]:
        if kind is None:
            return list(self._events)
        return [e for e in self._events if e.kind == kind]

    def errors(self) -> list[ObservableEvent]:
        return self.events(EventKind.ERROR)

    def intents(self) -> list[str]:
        return [e.payload.get("intent", "") for e in self.events(EventKind.INTENT)]

    def summary(self) -> dict[str, Any]:
        counts: dict[str, int] = {}
        for e in self._events:
            counts[e.kind.value] = counts.get(e.kind.value, 0) + 1
        return {
            "session_id": self.session_id,
            "total_events": len(self._events),
            "by_kind": counts,
            "error_count": counts.get("error", 0),
            "log_file": str(self._log_file) if self._log_file else None,
        }

    # ── Internals ─────────────────────────────────────────────────────────────

    @staticmethod
    def _detect_rich() -> bool:
        try:
            import rich  # noqa: F401
            return True
        except ImportError:
            return False


# ── Module-level convenience ──────────────────────────────────────────────────

def get_observer() -> Observer:
    """Return the process-wide Observer singleton."""
    return Observer.get()


def configure_verbosity(verbose: bool = True, quiet: bool = False, private: bool = False) -> None:
    """Apply --verbose / --quiet / --private CLI flag to the global observer."""
    obs = Observer.get()
    if private:
        obs.set_private()
    elif quiet:
        obs.set_quiet()
    else:
        obs.set_verbose()
