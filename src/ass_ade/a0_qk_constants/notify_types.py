"""Tier a0 — constants and TypedDicts for the notify subsystem."""

from __future__ import annotations

import enum
from typing import TypedDict


class NotifyChannel(str, enum.Enum):
    SLACK = "slack"
    DISCORD = "discord"
    WEBHOOK = "webhook"
    STDOUT = "stdout"   # for testing / local use


class NotifyPayload(TypedDict):
    text: str
    title: str
    level: str   # "info" | "success" | "warning" | "error"
    source: str  # which ass-ade command emitted this


NOTIFY_CONFIG_FILENAME = "notify.json"
NOTIFY_DIR_NAME = ".ass-ade"
NOTIFY_COLOR: dict[str, int] = {
    "info":    0x5865F2,
    "success": 0x57F287,
    "warning": 0xFEE75C,
    "error":   0xED4245,
}
