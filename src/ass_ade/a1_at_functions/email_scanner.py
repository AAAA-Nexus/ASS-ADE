"""Tier a1 — pure functions to parse, classify, and extract from email metadata."""

from __future__ import annotations

import re
import uuid
from datetime import datetime, timezone

from ass_ade.a0_qk_constants.assistant_types import EmailPriority, EmailSummary

# ------------------------------------------------------------------
# Priority classification heuristics (no ML needed)
# ------------------------------------------------------------------
_URGENT_SUBJECTS = re.compile(
    r"\b(urgent|asap|action required|critical|immediately|emergency|alert|incident|outage)\b",
    re.IGNORECASE,
)
_HIGH_SUBJECTS = re.compile(
    r"\b(important|follow.?up|deadline|overdue|reminder|review needed|please respond)\b",
    re.IGNORECASE,
)
_NEWSLETTER_DOMAINS = frozenset({
    "substack.com", "mailchimp.com", "sendgrid.net", "mailjet.com",
    "klaviyo.com", "constantcontact.com", "campaignmonitor.com",
    "beehiiv.com", "convertkit.com",
})
_NEWSLETTER_HEADERS = frozenset({
    "list-unsubscribe", "x-mailchimp", "x-campaign", "precedence",
})

_ACTION_PATTERNS = [
    re.compile(r"(?:please|can you|could you|need you to)\s+(.{10,80}?)(?:\.|$)", re.IGNORECASE),
    re.compile(r"(?:action item|todo|to-do|task)[:\s]+(.{5,100}?)(?:\.|$)", re.IGNORECASE),
    re.compile(r"(?:by|due|deadline)[:\s]+(.{5,60}?)(?:\.|$)", re.IGNORECASE),
]


def classify_priority(
    subject: str,
    sender: str = "",
    headers: dict[str, str] | None = None,
) -> EmailPriority:
    headers = headers or {}
    h_lower = {k.lower(): v for k, v in headers.items()}

    # Newsletter detection
    if any(k in h_lower for k in _NEWSLETTER_HEADERS):
        return EmailPriority.NEWSLETTER
    domain = sender.split("@")[-1].lower() if "@" in sender else ""
    if domain in _NEWSLETTER_DOMAINS:
        return EmailPriority.NEWSLETTER

    if _URGENT_SUBJECTS.search(subject):
        return EmailPriority.URGENT
    if _HIGH_SUBJECTS.search(subject):
        return EmailPriority.HIGH
    return EmailPriority.NORMAL


def extract_action_items(body: str) -> list[str]:
    """Pull candidate action items from an email body."""
    actions: list[str] = []
    for pat in _ACTION_PATTERNS:
        for m in pat.finditer(body):
            candidate = m.group(1).strip().rstrip(".,;")
            if 8 <= len(candidate) <= 120:
                actions.append(candidate)
    # Deduplicate while preserving order
    seen: set[str] = set()
    unique: list[str] = []
    for a in actions:
        low = a.lower()
        if low not in seen:
            seen.add(low)
            unique.append(a)
    return unique[:5]


def make_email_summary(
    subject: str,
    sender: str,
    date: str,
    body: str,
    message_id: str = "",
    headers: dict[str, str] | None = None,
    labels: list[str] | None = None,
) -> EmailSummary:
    priority = classify_priority(subject, sender, headers)
    action_items = extract_action_items(body)
    return EmailSummary(
        message_id=message_id or str(uuid.uuid4()),
        subject=subject,
        sender=sender,
        date=date,
        priority=priority.value,
        snippet=body[:200].replace("\n", " "),
        action_items=action_items,
        labels=labels or [],
    )


def format_email_row(email: EmailSummary) -> str:
    prio_icon = {"urgent": "🔴", "high": "🟡", "normal": "⚪", "low": "⬜", "newsletter": "📰"}.get(
        email["priority"], "⚪"
    )
    date_short = email["date"][:10]
    subject = email["subject"][:50]
    sender_short = email["sender"].split("<")[-1].rstrip(">")[:30]
    return f"{prio_icon} {date_short}  {sender_short:<30}  {subject}"
