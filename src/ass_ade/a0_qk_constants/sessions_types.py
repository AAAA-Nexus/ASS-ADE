"""Tier a0 — constants and TypedDicts for the sessions subsystem."""

from __future__ import annotations

import enum
from typing import TypedDict


class SessionState(str, enum.Enum):
    ACTIVE = "active"
    ARCHIVED = "archived"
    DELETED = "deleted"


class SessionRecord(TypedDict):
    id: str
    name: str
    created_at: str   # ISO-8601
    updated_at: str   # ISO-8601
    state: str        # SessionState value
    model: str
    message_count: int
    summary: str      # last AI turn, truncated


class MessageRecord(TypedDict):
    id: str
    session_id: str
    role: str         # "user" | "assistant"
    content: str
    ts: str           # ISO-8601


SESSIONS_DB_FILENAME = "sessions.db"
SESSIONS_DIR_NAME = ".ass-ade"
MAX_SUMMARY_LEN = 120
