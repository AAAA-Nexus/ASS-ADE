"""Tier a3 — session management service."""

from __future__ import annotations

from pathlib import Path

from ass_ade.a0_qk_constants.sessions_types import (
    MessageRecord,
    SessionRecord,
    SessionState,
)
from ass_ade.a1_at_functions.sessions_helpers import (
    filter_sessions,
    make_message_record,
    make_session_record,
)
from ass_ade.a2_mo_composites.sessions_store import SessionStore


class SessionsService:
    def __init__(self, db_path: Path | None = None) -> None:
        self._store = SessionStore(db_path)

    # ------------------------------------------------------------------
    # Session lifecycle
    # ------------------------------------------------------------------
    def new_session(self, name: str, model: str = "default") -> SessionRecord:
        rec = make_session_record(name, model=model)
        self._store.upsert_session(rec)
        return rec

    def list_sessions(
        self,
        *,
        include_archived: bool = False,
        query: str = "",
    ) -> list[SessionRecord]:
        state = None if include_archived else SessionState.ACTIVE
        records = self._store.list_sessions(state)
        return filter_sessions(records, query=query)

    def get_session(self, session_id: str) -> SessionRecord | None:
        # Support short-ID prefix lookup (first 8 chars)
        if len(session_id) < 36:
            all_sessions = self._store.list_sessions()
            matches = [s for s in all_sessions if s["id"].startswith(session_id)]
            if len(matches) == 1:
                return matches[0]
            if len(matches) > 1:
                raise ValueError(f"Ambiguous session prefix {session_id!r}: {len(matches)} matches")
            return None
        return self._store.get_session(session_id)

    def archive_session(self, session_id: str) -> None:
        self._store.set_state(session_id, SessionState.ARCHIVED)

    def delete_session(self, session_id: str) -> None:
        self._store.set_state(session_id, SessionState.DELETED)

    def restore_session(self, session_id: str) -> None:
        self._store.set_state(session_id, SessionState.ACTIVE)

    # ------------------------------------------------------------------
    # Messages
    # ------------------------------------------------------------------
    def add_message(self, session_id: str, role: str, content: str) -> MessageRecord:
        msg = make_message_record(session_id, role, content)
        self._store.append_message(msg)
        return msg

    def get_history(self, session_id: str, limit: int = 50) -> list[MessageRecord]:
        return self._store.get_history(session_id, limit=limit)

    def close(self) -> None:
        self._store.close()
