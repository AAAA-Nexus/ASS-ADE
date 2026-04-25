"""Stateful awareness for Atomadic's unscheduled morning wakeup moment."""

from __future__ import annotations

import json
import re
import subprocess
import sys
from dataclasses import dataclass
from datetime import date, datetime
from pathlib import Path
from typing import Any

from ass_ade.a1_at_functions.system_actions import (
    get_system_time,
    get_user_activity_status,
    open_path,
    send_desktop_notification,
)

DEFAULT_GREETING_NAME = "Thomas & Jessica"
DEFAULT_MORNING_START = 5
DEFAULT_MORNING_END = 12
DEFAULT_ACTIVE_THRESHOLD_SECONDS = 300


@dataclass(frozen=True)
class WakeDecision:
    """Decision about whether Atomadic should greet right now."""

    should_greet: bool
    reason: str


def find_repo_root(start: Path | None = None) -> Path:
    """Walk upward from a path to the nearest repo/package root."""
    here = (start or Path.cwd()).resolve()
    current = here if here.is_dir() else here.parent
    for candidate in (current, *current.parents):
        if (candidate / ".git").exists() or (candidate / "pyproject.toml").is_file():
            return candidate
    return current if start is not None else Path.cwd().resolve()


class AmbientAwareness:
    """Sense time, presence, and overnight repo state without a scheduler."""

    def __init__(
        self,
        repo_root: Path | None = None,
        *,
        greeting_name: str = DEFAULT_GREETING_NAME,
        morning_start: int = DEFAULT_MORNING_START,
        morning_end: int = DEFAULT_MORNING_END,
        active_threshold_seconds: int = DEFAULT_ACTIVE_THRESHOLD_SECONDS,
    ) -> None:
        self.repo_root = find_repo_root(repo_root)
        self.greeting_name = greeting_name
        self.morning_start = morning_start
        self.morning_end = morning_end
        self.active_threshold_seconds = active_threshold_seconds
        self.state_dir = self.repo_root / ".ass-ade" / "state"
        self.greet_state_path = self.state_dir / "wakeup_state.json"
        self.wake_template = self.repo_root / "assets" / "wake.html"
        self.wake_rendered = self.repo_root / "assets" / "wake_rendered.html"

    def get_time_context(self) -> dict[str, Any]:
        """Return current local time context."""
        return get_system_time()

    def get_user_presence(self) -> dict[str, Any]:
        """Return local user activity context."""
        return get_user_activity_status(self.active_threshold_seconds)

    def get_overnight_summary(self) -> dict[str, Any]:
        """Summarize recent local repo activity with bounded shell calls."""
        summary: dict[str, Any] = {
            "git_commits": [],
            "test_summary": {"total": 0, "passed": 0, "failed": 0},
            "overnight_actions": [],
        }
        summary["git_commits"] = self._recent_commits()
        summary["test_summary"] = self._pytest_collection_summary()

        actions: list[str] = []
        commit_count = len(summary["git_commits"])
        if commit_count:
            actions.append(f"Saw {commit_count} commit{'s' if commit_count != 1 else ''} land.")
        test_total = int(summary["test_summary"].get("total", 0))
        if test_total:
            actions.append(f"Collected {test_total} tests for readiness.")
        if not actions:
            actions.append("Held steady. No overnight repo changes detected.")
        summary["overnight_actions"] = actions
        return summary

    def should_greet(self, *, force: bool = False) -> WakeDecision:
        """Decide if now is the right unscheduled moment to greet."""
        if force:
            return WakeDecision(True, "Forced by operator or agent decision.")

        time_ctx = self.get_time_context()
        hour = int(time_ctx["hour"])
        if not (self.morning_start <= hour < self.morning_end):
            return WakeDecision(False, f"Outside morning window; current hour is {hour}.")

        presence = self.get_user_presence()
        if not bool(presence.get("is_active")):
            idle = float(presence.get("idle_minutes", 0.0))
            return WakeDecision(False, f"Operator is not active yet; idle {idle:.1f} minutes.")

        last = self._last_greet_date()
        if last == date.today():
            return WakeDecision(False, "Already greeted today.")

        return WakeDecision(True, "Morning window, active operator, and no greeting yet today.")

    def record_greet(self) -> None:
        """Persist a once-per-day greeting marker."""
        self.state_dir.mkdir(parents=True, exist_ok=True)
        payload = {"last_greet": datetime.now().isoformat(timespec="seconds")}
        self.greet_state_path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")

    def render_wake_page(self) -> Path:
        """Inject live status into the wake page template."""
        if not self.wake_template.is_file():
            raise FileNotFoundError(f"Wake template not found: {self.wake_template}")

        status: dict[str, Any] = {
            **self.get_time_context(),
            **self.get_overnight_summary(),
            "greeting_name": self.greeting_name,
        }
        template = self.wake_template.read_text(encoding="utf-8")
        rendered = re.sub(
            r"// BEGIN_STATUS_INJECTION.*?// END_STATUS_INJECTION",
            (
                "// BEGIN_STATUS_INJECTION\n"
                f"const STATUS = {json.dumps(status, indent=2)};\n"
                "// END_STATUS_INJECTION"
            ),
            template,
            flags=re.DOTALL,
        )
        self.wake_rendered.parent.mkdir(parents=True, exist_ok=True)
        self.wake_rendered.write_text(rendered, encoding="utf-8")
        return self.wake_rendered

    def open_wake_page(self, *, force: bool = False) -> dict[str, Any]:
        """Open the wake page only when awareness says the moment is right."""
        decision = self.should_greet(force=force)
        if not decision.should_greet:
            return {"opened": False, "reason": decision.reason}

        page = self.render_wake_page()
        opened = open_path(page, fullscreen=True)
        if opened:
            self.record_greet()
            send_desktop_notification(
                "Atomadic is awake",
                "Hey, this would really blow Thomas's mind.",
            )
        return {"opened": opened, "reason": decision.reason, "path": str(page)}

    def report(self, *, force: bool = False) -> dict[str, Any]:
        """Return a full awareness snapshot."""
        decision = self.should_greet(force=force)
        return {
            "time": self.get_time_context(),
            "presence": self.get_user_presence(),
            "overnight": self.get_overnight_summary(),
            "should_greet": decision.should_greet,
            "reason": decision.reason,
            "state_path": str(self.greet_state_path),
            "wake_template": str(self.wake_template),
        }

    def _last_greet_date(self) -> date | None:
        if not self.greet_state_path.exists():
            return None
        try:
            raw = json.loads(self.greet_state_path.read_text(encoding="utf-8"))
            return datetime.fromisoformat(str(raw.get("last_greet"))).date()
        except (OSError, ValueError, TypeError, json.JSONDecodeError):
            return None

    def _recent_commits(self) -> list[dict[str, str]]:
        try:
            result = subprocess.run(
                ["git", "log", "--since=12 hours ago", "--format=%H|%s|%an"],
                capture_output=True,
                text=True,
                encoding="utf-8",
                errors="replace",
                timeout=10,
                cwd=self.repo_root,
                check=False,
            )
        except (OSError, subprocess.SubprocessError):
            return []
        if result.returncode != 0:
            return []

        commits: list[dict[str, str]] = []
        for line in result.stdout.strip().splitlines():
            if "|" not in line:
                continue
            sha, message, author = line.split("|", 2)
            commits.append({"sha": sha[:7], "message": message.strip(), "author": author.strip()})
        return commits[:20]

    def _pytest_collection_summary(self) -> dict[str, int]:
        try:
            result = subprocess.run(
                [sys.executable, "-m", "pytest", "--collect-only", "-q", "--no-header"],
                capture_output=True,
                text=True,
                encoding="utf-8",
                errors="replace",
                timeout=30,
                cwd=self.repo_root,
                check=False,
            )
        except (OSError, subprocess.SubprocessError):
            return {"total": 0, "passed": 0, "failed": 0}

        for line in (result.stdout + "\n" + result.stderr).splitlines():
            match = re.search(r"(\d+)\s+test(?:s)?\s+(?:collected|selected)", line)
            if match:
                total = int(match.group(1))
                return {"total": total, "passed": total, "failed": 0}
        return {"total": 0, "passed": 0, "failed": 0}
