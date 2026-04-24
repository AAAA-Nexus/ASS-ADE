"""Tests for NexusSession — RatchetGate lifecycle."""

from __future__ import annotations

import hashlib
from unittest.mock import MagicMock

import pytest

from ass_ade.nexus.models import RatchetAdvance, RatchetSession, RatchetStatus
from ass_ade.nexus.session import NexusSession


def _mock_client() -> MagicMock:
    client = MagicMock()
    client.ratchet_register.return_value = RatchetSession(session_id="sess-abc", epoch=0)
    client.ratchet_advance.return_value = RatchetAdvance(new_epoch=1)
    client.ratchet_status.return_value = RatchetStatus(remaining_calls=42)
    return client


class TestNexusSession:
    def test_start_creates_session(self) -> None:
        session = NexusSession(_mock_client())
        result = session.start("13608")
        assert session.is_active
        assert session.session_id == "sess-abc"
        assert result.session_id == "sess-abc"

    def test_advance_increments_epoch(self) -> None:
        session = NexusSession(_mock_client())
        session.start("13608")
        session.advance()
        assert session.epoch == 1

    def test_advance_without_start_raises(self) -> None:
        session = NexusSession(_mock_client())
        with pytest.raises(RuntimeError, match="No active session"):
            session.advance()

    def test_status_without_start_raises(self) -> None:
        session = NexusSession(_mock_client())
        with pytest.raises(RuntimeError, match="No active session"):
            session.status()

    def test_is_healthy_true(self) -> None:
        session = NexusSession(_mock_client())
        session.start("13608")
        assert session.is_healthy()

    def test_is_healthy_false_when_no_calls(self) -> None:
        client = _mock_client()
        client.ratchet_status.return_value = RatchetStatus(remaining_calls=0)
        session = NexusSession(client)
        session.start("13608")
        assert not session.is_healthy()

    def test_teardown_resets_state(self) -> None:
        session = NexusSession(_mock_client())
        session.start("13608")
        session.teardown()
        assert not session.is_active
        assert session.session_id is None
        assert session.epoch == 0

    def test_start_non_numeric_agent_id_uses_deterministic_sha256_int(self) -> None:
        client = _mock_client()
        session = NexusSession(client)

        agent_id = "agent-alpha"
        expected = int.from_bytes(
            hashlib.sha256(agent_id.encode("utf-8")).digest()[:4],
            "big",
        ) & 0x7FFFFFFF

        session.start(agent_id)
        session.start(agent_id)

        assert client.ratchet_register.call_count == 2
        first_arg = client.ratchet_register.call_args_list[0].args[0]
        second_arg = client.ratchet_register.call_args_list[1].args[0]
        assert first_arg == expected
        assert second_arg == expected
