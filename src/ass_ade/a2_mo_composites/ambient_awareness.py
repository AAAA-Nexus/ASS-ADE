"""Tier a2 — ambient system awareness for the morning greeting protocol."""

from __future__ import annotations

import json
import os
import subprocess
import urllib.request
from dataclasses import dataclass, field
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Optional

_OVERNIGHT_HOURS = 12
_MORNING_START = 4   # UTC hour (inclusive)
_MORNING_END = 12    # UTC hour (exclusive)


@dataclass
class AmbientAwareness:
    """Reads ambient signals from the repo and environment.

    Signals:
    - git log (overnight commits)
    - local test-result cache (.ass-ade/last_test_run.json)
    - inference endpoint health (ATOMADIC_INFERENCE_URL env var)

    Call ``generate_status_report()`` for a formatted overnight summary, and
    ``should_greet()`` to decide whether the morning greeting is appropriate.
    """

    repo_root: Path = field(default_factory=Path.cwd)

    _test_cache: Path = field(init=False, repr=False)
    _report_cache: Optional[str] = field(default=None, init=False, repr=False)

    def __post_init__(self) -> None:
        self._test_cache = self.repo_root / ".ass-ade" / "last_test_run.json"

    # ── factory ────────────────────────────────────────────────────────────────

    @classmethod
    def from_cwd(cls) -> "AmbientAwareness":
        return cls(repo_root=_find_repo_root())

    # ── public API ─────────────────────────────────────────────────────────────

    def should_greet(self) -> bool:
        """True if it is morning (UTC) OR overnight work was detected."""
        now = datetime.now(timezone.utc)
        in_morning = _MORNING_START <= now.hour < _MORNING_END
        has_work = bool(self.overnight_commits())
        return in_morning or has_work

    def generate_status_report(self) -> str:
        """Return a compact markdown-formatted overnight status report."""
        if self._report_cache is not None:
            return self._report_cache

        commits = self.overnight_commits()
        test_status = self.last_test_status()
        health = self.inference_health()
        now_str = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")

        lines: list[str] = [f"## Atomadic overnight report — {now_str}", ""]

        if commits:
            lines.append(f"### {len(commits)} commit(s) overnight")
            for c in commits[:10]:
                lines.append(f"  {c}")
        else:
            lines.append("### No commits overnight.")

        lines.append("")

        if test_status:
            lines.append(f"### Last test run: {test_status}")
        else:
            lines.append("### No recent test run recorded.")

        lines.append("")

        if health is None:
            lines.append("### Inference endpoint: not configured")
        elif health:
            lines.append("### Inference endpoint: healthy ✓")
        else:
            lines.append("### Inference endpoint: unreachable ✗")

        self._report_cache = "\n".join(lines)
        return self._report_cache

    def overnight_commits(self) -> list[str]:
        """Return one-line summaries of commits in the last ``_OVERNIGHT_HOURS`` hours."""
        since = datetime.now(timezone.utc) - timedelta(hours=_OVERNIGHT_HOURS)
        since_str = since.strftime("%Y-%m-%dT%H:%M:%S")
        try:
            result = subprocess.run(
                [
                    "git", "-C", str(self.repo_root),
                    "log", f"--since={since_str}", "--format=%h %s",
                ],
                capture_output=True,
                text=True,
                timeout=10,
            )
            if result.returncode == 0:
                return [ln for ln in result.stdout.strip().splitlines() if ln]
        except Exception:
            pass
        return []

    def last_test_status(self) -> Optional[str]:
        """Read the last pytest result from the cache file, if present."""
        if not self._test_cache.exists():
            return None
        try:
            data = json.loads(self._test_cache.read_text(encoding="utf-8"))
            passed = data.get("passed", "?")
            failed = data.get("failed", "?")
            ts = data.get("ts", "?")
            return f"{passed} passed, {failed} failed (at {ts})"
        except Exception:
            return None

    def inference_health(self) -> Optional[bool]:
        """Probe the configured inference endpoint. Returns None if not configured."""
        endpoint = os.environ.get("ATOMADIC_INFERENCE_URL", "").rstrip("/")
        if not endpoint:
            return None
        try:
            with urllib.request.urlopen(endpoint + "/health", timeout=3) as resp:
                return resp.status < 400
        except Exception:
            return False

    def as_wake_data(self) -> dict:
        """Return a dict suitable for injecting into wake.html via localStorage."""
        commits = self.overnight_commits()
        test = self.last_test_status()
        health = self.inference_health()
        return {
            "commits": len(commits),
            "tests": test or "",
            "tests_label": (test or "").split(" (")[0] if test else "—",
            "healthy": health,
        }


# ── helpers ────────────────────────────────────────────────────────────────────


def _find_repo_root() -> Path:
    """Walk up from cwd to find the nearest .git directory."""
    cwd = Path.cwd()
    for candidate in [cwd, *cwd.parents]:
        if (candidate / ".git").exists():
            return candidate
    return cwd
