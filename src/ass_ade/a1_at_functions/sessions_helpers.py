"""Tier a1 — pure helpers for the sessions subsystem."""

from __future__ import annotations

import uuid
from datetime import datetime, timezone
from typing import Sequence

from ass_ade.a0_qk_constants.sessions_types import (
    MAX_SUMMARY_LEN,
    MessageRecord,
    SessionRecord,
    SessionState,
)


def new_session_id() -> str:
    return str(uuid.uuid4())


def now_iso() -> str:
    return datetime.now(tz=timezone.utc).isoformat(timespec="seconds")


def truncate_summary(text: str) -> str:
    if len(text) <= MAX_SUMMARY_LEN:
        return text
    return text[:MAX_SUMMARY_LEN].rstrip() + "…"


def make_session_record(
    name: str,
    model: str = "default",
    state: SessionState = SessionState.ACTIVE,
) -> SessionRecord:
    now = now_iso()
    return SessionRecord(
        id=new_session_id(),
        name=name,
        created_at=now,
        updated_at=now,
        state=state.value,
        model=model,
        message_count=0,
        summary="",
    )


def make_message_record(session_id: str, role: str, content: str) -> MessageRecord:
    return MessageRecord(
        id=new_session_id(),
        session_id=session_id,
        role=role,
        content=content,
        ts=now_iso(),
    )


def format_session_row(rec: SessionRecord) -> str:
    marker = "●" if rec["state"] == SessionState.ACTIVE.value else "○"
    ts = rec["updated_at"][:10]
    summary = rec["summary"] or "(empty)"
    return f"{marker} [{rec['id'][:8]}] {rec['name']:<24} {ts}  {summary}"


def format_history_row(msg: MessageRecord, idx: int) -> str:
    role = msg["role"].upper()[:9].ljust(9)
    ts = msg["ts"][11:16]  # HH:MM
    snippet = msg["content"][:80].replace("\n", " ")
    return f"  {idx:>3}. [{ts}] {role}  {snippet}"


def filter_sessions(
    records: Sequence[SessionRecord],
    *,
    state: SessionState | None = None,
    query: str = "",
) -> list[SessionRecord]:
    out = list(records)
    if state is not None:
        out = [r for r in out if r["state"] == state.value]
    if query:
        q = query.lower()
        out = [r for r in out if q in r["name"].lower() or q in r["summary"].lower()]
    return out
