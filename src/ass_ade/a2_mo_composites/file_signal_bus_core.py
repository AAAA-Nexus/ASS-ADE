"""Tier a2 — assimilated class 'FileSignalBus'

Assimilated from: bus.py:51-224
"""

from __future__ import annotations


# --- assimilated symbol ---
class FileSignalBus:
    """Filesystem-backed signal bus.

    Parameters
    ----------
    root:
        Directory that will hold ``inbox/``, ``read/``, ``acks/``, and the
        append-only log. Created on first use.
    agent_id:
        Identity of the caller. Required for ``unread`` and ``ack`` so that
        per-agent delivery tracking is unambiguous.
    now:
        Optional zero-arg callable returning a timezone-aware UTC datetime.
        Injectable so tests can pin the clock without monkeypatching.
    """

    def __init__(
        self,
        root: Path,
        agent_id: str,
        *,
        now=None,
    ) -> None:
        self.root = Path(root)
        self.agent_id = agent_id or "anonymous"
        self._now = now or (lambda: _dt.datetime.now(_dt.UTC))
        self._ensure_layout()

    # --- layout ---------------------------------------------------------------

    def _ensure_layout(self) -> None:
        (self.root / "inbox").mkdir(parents=True, exist_ok=True)
        (self.root / "read").mkdir(parents=True, exist_ok=True)
        (self.root / "acks").mkdir(parents=True, exist_ok=True)

    @property
    def inbox_dir(self) -> Path:
        return self.root / "inbox"

    @property
    def log_path(self) -> Path:
        return self.root / "broadcast.log.jsonl"

    def _delivery_marker(self, sid: str, agent_id: str | None = None) -> Path:
        agent = agent_id or self.agent_id
        return self.root / "read" / _slug(agent) / f"{sid}.delivered"

    def _ack_path(self, sid: str, agent_id: str | None = None) -> Path:
        agent = agent_id or self.agent_id
        return self.root / "acks" / _slug(agent) / f"{sid}.ack.md"

    # --- publish --------------------------------------------------------------

    def broadcast(self, signal: Signal) -> SignalEnvelope:
        """Write a signal to the inbox and log it. Returns the envelope."""
        now = self._now()
        envelope = render_envelope(
            signal,
            issued_at_compact=now.strftime("%Y%m%dT%H%M%SZ"),
            issued_at_rfc3339=now.strftime("%Y-%m-%dT%H:%M:%SZ"),
        )
        target = self.inbox_dir / f"{envelope.signal_id}.md"
        _atomic_write_text(target, serialize_envelope(envelope))
        self._append_log({
            "ts": envelope.issued_at,
            "event": "broadcast",
            "signal_id": envelope.signal_id,
            "priority": envelope.priority.value,
            "issued_by": envelope.issued_by,
            "routes": list(envelope.routes),
            "digest": envelope.digest,
        })
        return envelope

    # --- consume --------------------------------------------------------------

    def list_inbox(self) -> list[SignalEnvelope]:
        """Return every well-formed signal in the inbox, oldest first."""
        envelopes: list[SignalEnvelope] = []
        for path in sorted(self.inbox_dir.glob("*.md")):
            try:
                envelopes.append(parse_envelope(path.read_text(encoding="utf-8")))
            except (MalformedSignalError, OSError) as e:
                self._append_log({
                    "ts": _rfc3339(self._now()),
                    "event": "parse_error",
                    "path": str(path),
                    "error": f"{type(e).__name__}: {e}",
                })
        return envelopes

    def unread(self) -> list[DeliveryReceipt]:
        """Return signals routed to this agent that have not been delivered yet.

        Side-effect: each returned signal is marked as delivered for the
        current ``agent_id`` so a subsequent call returns an empty list unless
        a new broadcast has landed. Use ``peek`` for a side-effect-free read.
        """
        now_iso = _rfc3339(self._now())
        receipts: list[DeliveryReceipt] = []
        for env in self.list_inbox():
            if not env.matches(self.agent_id):
                continue
            if env.is_expired(now_iso):
                continue
            marker = self._delivery_marker(env.signal_id)
            already = marker.exists()
            if already:
                continue
            _atomic_write_text(marker, now_iso + "\n")
            self._append_log({
                "ts": now_iso, "event": "delivered",
                "agent": self.agent_id, "signal_id": env.signal_id,
                "priority": env.priority.value,
            })
            receipts.append(DeliveryReceipt(envelope=env,
                                            was_delivered_before=False,
                                            delivered_to=self.agent_id))
        return receipts

    def peek(self) -> list[SignalEnvelope]:
        """Like ``unread`` but without marking anything as delivered."""
        now_iso = _rfc3339(self._now())
        out: list[SignalEnvelope] = []
        for env in self.list_inbox():
            if not env.matches(self.agent_id):
                continue
            if env.is_expired(now_iso):
                continue
            if self._delivery_marker(env.signal_id).exists():
                continue
            out.append(env)
        return out

    # --- acknowledge ----------------------------------------------------------

    def ack(self, signal_id: str, note: str = "") -> AckRecord:
        """Persist an acknowledgement for ``signal_id`` under this agent."""
        record = AckRecord(
            signal_id=signal_id,
            ack_by=self.agent_id,
            ack_at=_rfc3339(self._now()),
            note=note.strip(),
        )
        ack_path = self._ack_path(signal_id)
        content = (
            "---\n"
            f"signal_id: {record.signal_id}\n"
            f"ack_by: {record.ack_by}\n"
            f"ack_at: {record.ack_at}\n"
            "---\n"
            "\n"
            f"{record.note}\n"
        )
        _atomic_write_text(ack_path, content)
        self._append_log({
            "ts": record.ack_at, "event": "ack",
            "agent": record.ack_by, "signal_id": record.signal_id,
            "note": record.note,
        })
        return record

    # --- audit log ------------------------------------------------------------

    def _append_log(self, event: dict) -> None:
        self.log_path.parent.mkdir(parents=True, exist_ok=True)
        with self.log_path.open("a", encoding="utf-8", newline="\n") as f:
            f.write(json.dumps(event, sort_keys=True) + "\n")

    def iter_log(self) -> Iterable[dict]:
        if not self.log_path.exists():
            return iter(())
        with self.log_path.open("r", encoding="utf-8") as f:
            return [json.loads(line) for line in f if line.strip()]  # type: ignore[return-value]

