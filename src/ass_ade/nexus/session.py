"""RatchetGate session lifecycle manager.

Wraps the RatchetGate endpoints into a coherent session object so
CLI commands and workflows can manage forward-secret sessions without
manually juggling session IDs and epochs.
"""

from __future__ import annotations

import hashlib

from ass_ade.nexus.client import NexusClient
from ass_ade.nexus.errors import NexusError
from ass_ade.nexus.models import RatchetAdvance, RatchetSession, RatchetStatus
from ass_ade.nexus.validation import validate_agent_id, validate_session_id


class NexusSession:
    """Manages a single RatchetGate session lifecycle."""

    def __init__(self, client: NexusClient) -> None:
        self._client = client
        self.session_id: str | None = None
        self.epoch: int = 0
        self._started = False

    @property
    def is_active(self) -> bool:
        return self._started and self.session_id is not None

    def start(self, agent_id: str) -> RatchetSession:
        """Register a new RatchetGate session."""
        validate_agent_id(agent_id)
        # RatchetGate enforces the structural-parity invariant `AN-TH-STRUCT-PARITY` server-side;
        # we send the raw value and let the server reject non-conforming IDs.
        result = self._client.ratchet_register(
            int(agent_id) if agent_id.isdigit() else (
                int.from_bytes(hashlib.sha256(agent_id.encode("utf-8")).digest()[:4], "big") & 0x7FFFFFFF
            )
        )
        self.session_id = result.session_id
        self.epoch = result.epoch or 0
        self._started = True
        return result

    def advance(self) -> RatchetAdvance:
        """Advance the session epoch and re-key."""
        if not self.is_active:
            raise RuntimeError("No active session. Call start() first.")
        if self.session_id is None:
            raise RuntimeError("session_id must not be None")
        validate_session_id(self.session_id)
        result = self._client.ratchet_advance(self.session_id)
        self.epoch = result.new_epoch or self.epoch + 1
        return result

    def status(self) -> RatchetStatus:
        """Check current session health."""
        if not self.is_active:
            raise RuntimeError("No active session. Call start() first.")
        if self.session_id is None:
            raise RuntimeError("session_id must not be None")
        validate_session_id(self.session_id)
        return self._client.ratchet_status(self.session_id)

    def is_healthy(self) -> bool:
        """Return True if the session is active and has remaining calls."""
        if not self.is_active:
            return False
        try:
            s = self.status()
            remaining = s.remaining_calls
            return remaining is None or remaining > 0
        except NexusError:
            return False

    def teardown(self) -> None:
        """Mark the session as ended (client-side only)."""
        self.session_id = None
        self.epoch = 0
        self._started = False
