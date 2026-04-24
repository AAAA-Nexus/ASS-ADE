"""Tier a2 — SQLite-backed session store."""

from __future__ import annotations

import sqlite3
from pathlib import Path
from typing import Sequence

from ass_ade.a0_qk_constants.sessions_types import (
    SESSIONS_DB_FILENAME,
    SESSIONS_DIR_NAME,
    MessageRecord,
    SessionRecord,
    SessionState,
)
from ass_ade.a1_at_functions.sessions_helpers import now_iso, truncate_summary


def _default_db_path() -> Path:
    base = Path.home() / SESSIONS_DIR_NAME
    base.mkdir(parents=True, exist_ok=True)
    return base / SESSIONS_DB_FILENAME


class SessionStore:
    def __init__(self, db_path: Path | None = None) -> None:
        self._path = db_path or _default_db_path()
        self._conn = sqlite3.connect(str(self._path), check_same_thread=False)
        self._conn.row_factory = sqlite3.Row
        self._migrate()

    # ------------------------------------------------------------------
    # Schema
    # ------------------------------------------------------------------
    def _migrate(self) -> None:
        self._conn.executescript("""
            CREATE TABLE IF NOT EXISTS sessions (
                id           TEXT PRIMARY KEY,
                name         TEXT NOT NULL,
                created_at   TEXT NOT NULL,
                updated_at   TEXT NOT NULL,
                state        TEXT NOT NULL DEFAULT 'active',
                model        TEXT NOT NULL DEFAULT 'default',
                message_count INTEGER NOT NULL DEFAULT 0,
                summary      TEXT NOT NULL DEFAULT ''
            );
            CREATE TABLE IF NOT EXISTS messages (
                id         TEXT PRIMARY KEY,
                session_id TEXT NOT NULL REFERENCES sessions(id),
                role       TEXT NOT NULL,
                content    TEXT NOT NULL,
                ts         TEXT NOT NULL
            );
            CREATE INDEX IF NOT EXISTS ix_messages_session ON messages(session_id, ts);
        """)
        self._conn.commit()

    # ------------------------------------------------------------------
    # Sessions CRUD
    # ------------------------------------------------------------------
    def upsert_session(self, rec: SessionRecord) -> None:
        self._conn.execute(
            """
            INSERT INTO sessions (id, name, created_at, updated_at, state, model, message_count, summary)
            VALUES (:id,:name,:created_at,:updated_at,:state,:model,:message_count,:summary)
            ON CONFLICT(id) DO UPDATE SET
                name=excluded.name, updated_at=excluded.updated_at,
                state=excluded.state, model=excluded.model,
                message_count=excluded.message_count, summary=excluded.summary
            """,
            dict(rec),
        )
        self._conn.commit()

    def get_session(self, session_id: str) -> SessionRecord | None:
        row = self._conn.execute(
            "SELECT * FROM sessions WHERE id=?", (session_id,)
        ).fetchone()
        return dict(row) if row else None  # type: ignore[return-value]

    def list_sessions(self, state: SessionState | None = None) -> list[SessionRecord]:
        if state is None:
            rows = self._conn.execute(
                "SELECT * FROM sessions ORDER BY updated_at DESC"
            ).fetchall()
        else:
            rows = self._conn.execute(
                "SELECT * FROM sessions WHERE state=? ORDER BY updated_at DESC",
                (state.value,),
            ).fetchall()
        return [dict(r) for r in rows]  # type: ignore[return-value]

    def set_state(self, session_id: str, state: SessionState) -> None:
        self._conn.execute(
            "UPDATE sessions SET state=?, updated_at=? WHERE id=?",
            (state.value, now_iso(), session_id),
        )
        self._conn.commit()

    # ------------------------------------------------------------------
    # Messages
    # ------------------------------------------------------------------
    def append_message(self, msg: MessageRecord) -> None:
        self._conn.execute(
            "INSERT INTO messages (id,session_id,role,content,ts) VALUES (?,?,?,?,?)",
            (msg["id"], msg["session_id"], msg["role"], msg["content"], msg["ts"]),
        )
        summary = truncate_summary(msg["content"]) if msg["role"] == "assistant" else None
        if summary is not None:
            self._conn.execute(
                "UPDATE sessions SET message_count=message_count+1, updated_at=?, summary=? WHERE id=?",
                (now_iso(), summary, msg["session_id"]),
            )
        else:
            self._conn.execute(
                "UPDATE sessions SET message_count=message_count+1, updated_at=? WHERE id=?",
                (now_iso(), msg["session_id"]),
            )
        self._conn.commit()

    def get_history(self, session_id: str, limit: int = 50) -> list[MessageRecord]:
        rows = self._conn.execute(
            "SELECT * FROM messages WHERE session_id=? ORDER BY ts DESC LIMIT ?",
            (session_id, limit),
        ).fetchall()
        return list(reversed([dict(r) for r in rows]))  # type: ignore[return-value]

    def close(self) -> None:
        self._conn.close()
