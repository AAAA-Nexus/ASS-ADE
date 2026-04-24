"""Tier a1 — pure helpers for the cron subsystem."""

from __future__ import annotations

import re
import uuid
from datetime import datetime, timezone

from ass_ade.a0_qk_constants.cron_types import (
    CRON_ALIASES,
    CronJob,
    CronState,
)

_CRON_FIELD_RE = re.compile(
    r"^(\*|[0-9]+(-[0-9]+)?(,[0-9]+(-[0-9]+)?)*|(\*/[0-9]+))$"
)


def resolve_schedule(schedule: str) -> str:
    """Expand @-aliases to full cron expressions."""
    return CRON_ALIASES.get(schedule.strip(), schedule.strip())


def validate_schedule(schedule: str) -> str | None:
    """Return None if valid, or an error string if not."""
    expr = resolve_schedule(schedule)
    parts = expr.split()
    if len(parts) != 5:
        return f"Expected 5 fields (min hour dom mon dow), got {len(parts)}: {expr!r}"
    ranges = [(0, 59), (0, 23), (1, 31), (1, 12), (0, 7)]
    labels = ["minute", "hour", "day-of-month", "month", "day-of-week"]
    for field, (lo, hi), label in zip(parts, ranges, labels):
        if not _CRON_FIELD_RE.match(field):
            return f"Invalid {label} field: {field!r}"
        for part in field.replace("*/", "").split(","):
            for num in part.split("-"):
                if num.isdigit() and not (lo <= int(num) <= hi):
                    return f"{label} value {num} out of range [{lo},{hi}]"
    return None


def make_cron_job(name: str, schedule: str, command: str) -> CronJob:
    return CronJob(
        id=str(uuid.uuid4()),
        name=name,
        schedule=resolve_schedule(schedule),
        command=command,
        state=CronState.ENABLED.value,
        created_at=datetime.now(tz=timezone.utc).isoformat(timespec="seconds"),
        last_run="",
        last_exit=-1,
        run_count=0,
    )


def format_cron_row(job: CronJob) -> str:
    state_icon = "●" if job["state"] == CronState.ENABLED.value else "○"
    last = job["last_run"][:10] if job["last_run"] else "never"
    exit_str = f"exit={job['last_exit']}" if job["run_count"] > 0 else "not-run"
    return (
        f"{state_icon} [{job['id'][:8]}] {job['name']:<20} "
        f"{job['schedule']:<15} {last:<12} {exit_str:<10}  {job['command']}"
    )


def next_run_hint(schedule: str) -> str:
    """Very lightweight human hint — does NOT do full cron math."""
    aliases_rev = {v: k for k, v in CRON_ALIASES.items()}
    if schedule in aliases_rev:
        return aliases_rev[schedule]
    parts = schedule.split()
    if parts == ["0", "0", "*", "*", "*"]:
        return "daily at midnight"
    if parts == ["0", "9", "*", "*", "*"]:
        return "daily at 09:00"
    return schedule
