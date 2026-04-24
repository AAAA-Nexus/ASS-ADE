"""Tier a0 — types for the personal assistant subsystem."""

from __future__ import annotations

import enum
from typing import TypedDict


class EmailPriority(str, enum.Enum):
    URGENT = "urgent"
    HIGH = "high"
    NORMAL = "normal"
    LOW = "low"
    NEWSLETTER = "newsletter"


class TaskStatus(str, enum.Enum):
    OPEN = "open"
    IN_PROGRESS = "in_progress"
    DONE = "done"


class InsightTag(str, enum.Enum):
    DECISION = "decision"
    ACTION = "action"
    QUESTION = "question"
    REFERENCE = "reference"
    IDEA = "idea"
    RISK = "risk"


class EmailSummary(TypedDict):
    message_id: str
    subject: str
    sender: str
    date: str           # ISO-8601
    priority: str       # EmailPriority value
    snippet: str        # first 200 chars of body
    action_items: list[str]
    labels: list[str]


class CalendarEvent(TypedDict):
    id: str
    title: str
    start: str          # ISO-8601
    end: str            # ISO-8601
    location: str
    attendees: list[str]
    description: str
    source: str         # "google" | "ical" | "manual"


class TaskItem(TypedDict):
    id: str
    title: str
    source: str         # filename or conversation ID where it was extracted
    status: str         # TaskStatus value
    priority: str       # "high" | "normal" | "low"
    due: str            # ISO-8601 or ""
    created_at: str     # ISO-8601
    tags: list[str]


class DocumentMetadata(TypedDict):
    path: str
    title: str
    size_bytes: int
    modified: str       # ISO-8601
    doc_type: str       # "markdown" | "pdf" | "txt" | "code" | "other"
    summary: str        # first 500 chars
    tags: list[str]


class Insight(TypedDict):
    id: str
    text: str
    tag: str            # InsightTag value
    source: str         # filename or conversation
    confidence: float   # 0.0–1.0
    created_at: str     # ISO-8601
    hash: str           # SHA-256 of text for dedup


# Directory + file constants
ASSISTANT_DIR = ".ass-ade/assistant"
TASKS_FILENAME = "tasks.json"
INSIGHTS_FILENAME = "insights.json"
HARVEST_REPORT_FILENAME = "harvest_report.json"
