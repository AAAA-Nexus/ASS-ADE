"""Tier a0 — constants and dataclasses for the cron subsystem."""

from __future__ import annotations

import enum
from typing import TypedDict


class CronState(str, enum.Enum):
    ENABLED = "enabled"
    DISABLED = "disabled"


class CronJob(TypedDict):
    id: str
    name: str
    schedule: str        # cron expression: "0 9 * * *"
    command: str         # shell command or ass-ade subcommand
    state: str           # CronState value
    created_at: str      # ISO-8601
    last_run: str        # ISO-8601 or ""
    last_exit: int       # -1 = never run
    run_count: int


CRON_STORE_FILENAME = "cron.json"
CRON_DIR_NAME = ".ass-ade"

# Supported special schedule strings
CRON_ALIASES: dict[str, str] = {
    "@hourly":   "0 * * * *",
    "@daily":    "0 0 * * *",
    "@midnight": "0 0 * * *",
    "@weekly":   "0 0 * * 0",
    "@monthly":  "0 0 1 * *",
    "@yearly":   "0 0 1 1 *",
    "@annually": "0 0 1 1 *",
}
