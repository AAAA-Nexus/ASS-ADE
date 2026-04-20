"""Tests for the A2A agent card interop module."""

from __future__ import annotations

import json
from unittest.mock import MagicMock, patch

import pytest

from ass_ade.a2a import (
    A2AAgentCard,
    A2AAuthentication,
    A2ASkill,
    ValidationIssue,
    ValidationReport,
    fetch_agent_card,
    local_agent_card,
    negotiate,
    validate_agent_card,
)

# ── validate_agent_card ──────────────────────────────────────────────────────


class TestValidateAgentCard:
    def test_valid_minimal_card(self) -> None:
        data = {"name": "TestAgent"}
        report = validate_agent_card(data)
        assert report.valid
        assert report.card is not None
        assert report.card.name == "TestAgent"

    def test_valid_full_card(self) -> None:
        data = {
            "name": "FullAgent",
            "description": "A complete agent",
            "url": "https://example.com",
            "version": "1.0.0",
            "provider": {"organization": "TestOrg", "url": "https://testorg.com"},
            "capabilities": {"streaming": True, "pushNotifications": False, "stateTransitionHistory": True},
            "authentication": {"schemes": ["bearer"]},
            "skills": [
                {"id": "skill1", "name": "Skill One", "description": "Does things"},
            ],
            "defaultInputModes": ["text/plain"],
            "defaultOutputModes": ["text/plain", "application/json"],
        }
        report = validate_agent_card(data)
        assert report.valid
        assert report.card is not None
        assert report.card.name == "FullAgent"
        assert report.card.capabilities.streaming is True
        assert len(report.card.skills) == 1
        assert report.card.skills[0].id == "skill1"

    def test_missing_name_is_error(self) -> None:
        data = {"description": "no name"}
        report = validate_agent_card(data)
        assert not report.valid
        assert any(i.severity == "error" for i in report.issues)

    def test_empty_name_is_error(self) -> None:
        data = {"name": "   "}
        report = validate_agent_card(data)
        assert not report.valid

    def test_missing_description_is_warning(self) -> None:
        data = {"name": "TestAgent", "url": "https://example.com", "version": "1.0"}
        report = validate_agent_card(data)
        assert report.valid
        assert any(i.severity == "warning" and i.field == "description" for i in report.issues)

    def test_missing_url_is_warning(self) -> None:
        data = {"name": "TestAgent", "description": "desc"}
        report = validate_agent_card(data)
        assert report.valid
        assert any(i.severity == "warning" and i.field == "url" for i in report.issues)

    def test_invalid_url_scheme_is_error(self) -> None:
        data = {"name": "TestAgent", "url": "ftp://bad.com"}
        report = validate_agent_card(data)
        assert not report.valid
        assert any("scheme" in i.message for i in report.errors)

    def test_missing_version_is_warning(self) -> None:
        data = {"name": "TestAgent", "url": "https://example.com"}
        report = validate_agent_card(data)
        assert any(i.severity == "warning" and i.field == "version" for i in report.issues)

    def test_no_skills_is_warning(self) -> None:
        data = {"name": "TestAgent", "url": "https://example.com", "version": "1.0", "description": "desc"}
        report = validate_agent_card(data)
        assert any(i.severity == "warning" and i.field == "skills" for i in report.issues)

    def test_skill_missing_id_is_error(self) -> None:
        data = {
            "name": "TestAgent",
            "url": "https://example.com",
            "version": "1.0",
            "skills": [{"id": "", "name": "Skill One"}],
        }
        report = validate_agent_card(data)
        assert not report.valid

    def test_skill_missing_name_is_error(self) -> None:
        data = {
            "name": "TestAgent",
            "url": "https://example.com",
            "version": "1.0",
            "skills": [{"id": "s1", "name": ""}],
        }
        report = validate_agent_card(data)
        assert not report.valid

    def test_auth_no_schemes_is_warning(self) -> None:
        data = {"name": "TestAgent", "authentication": {"schemes": []}}
        report = validate_agent_card(data)
        assert any(i.severity == "warning" and "schemes" in i.field for i in report.issues)


# ── fetch_agent_card ─────────────────────────────────────────────────────────


_FAKE_ADDR_INFO = [(None, None, None, None, ("93.184.216.34", None))]


class TestFetchAgentCard:
    def test_fetch_success(self) -> None:
        card_data = {"name": "RemoteAgent", "description": "A remote agent", "url": "https://remote.com", "version": "2.0"}
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = card_data

        with patch("ass_ade.a2a.socket.getaddrinfo", return_value=_FAKE_ADDR_INFO):
            with patch("ass_ade.a2a.httpx.get", return_value=mock_response) as mock_get:
                report = fetch_agent_card("https://remote.com")
                mock_get.assert_called_once_with(
                    "https://remote.com/.well-known/agent.json",
                    timeout=10.0,
                    follow_redirects=False,
                )
                assert report.valid
                assert report.card is not None
                assert report.card.name == "RemoteAgent"

    def test_fetch_appends_well_known_path(self) -> None:
        mock_response = MagicMock()
        mock_response.json.return_value = {"name": "Test"}

        with patch("ass_ade.a2a.socket.getaddrinfo", return_value=_FAKE_ADDR_INFO):
            with patch("ass_ade.a2a.httpx.get", return_value=mock_response) as mock_get:
                fetch_agent_card("https://example.com/")
                mock_get.assert_called_once_with(
                    "https://example.com/.well-known/agent.json",
                    timeout=10.0,
                    follow_redirects=False,
                )

    def test_fetch_does_not_duplicate_well_known(self) -> None:
        mock_response = MagicMock()
        mock_response.json.return_value = {"name": "Test"}

        with patch("ass_ade.a2a.socket.getaddrinfo", return_value=_FAKE_ADDR_INFO):
            with patch("ass_ade.a2a.httpx.get", return_value=mock_response) as mock_get:
                fetch_agent_card("https://example.com/.well-known/agent.json")
                mock_get.assert_called_once_with(
                    "https://example.com/.well-known/agent.json",
                    timeout=10.0,
                    follow_redirects=False,
                )

    def test_fetch_http_error(self) -> None:
        import httpx as _httpx

        mock_response = MagicMock()
        mock_response.status_code = 404
        error = _httpx.HTTPStatusError("Not Found", request=MagicMock(), response=mock_response)

        with patch("ass_ade.a2a.socket.getaddrinfo", return_value=_FAKE_ADDR_INFO):
            with patch("ass_ade.a2a.httpx.get", side_effect=error):
                report = fetch_agent_card("https://bad.com")
                assert not report.valid
                assert any("404" in i.message for i in report.errors)

    def test_fetch_network_error(self) -> None:
        import httpx as _httpx

        with patch("ass_ade.a2a.socket.getaddrinfo", return_value=_FAKE_ADDR_INFO):
            with patch("ass_ade.a2a.httpx.get", side_effect=_httpx.ConnectError("refused")):
                report = fetch_agent_card("https://unreachable.com")
                assert not report.valid
                assert any("Network" in i.message for i in report.errors)

    def test_fetch_invalid_json(self) -> None:
        mock_response = MagicMock()
        mock_response.json.side_effect = json.JSONDecodeError("", "", 0)

        with patch("ass_ade.a2a.socket.getaddrinfo", return_value=_FAKE_ADDR_INFO):
            with patch("ass_ade.a2a.httpx.get", return_value=mock_response):
                report = fetch_agent_card("https://bad-json.com")
                assert not report.valid
                assert any("JSON" in i.message for i in report.errors)


# ── negotiate ────────────────────────────────────────────────────────────────


class TestNegotiate:
    def _make_card(
        self,
        name: str = "Agent",
        skills: list[tuple[str, str]] | None = None,
        auth_schemes: list[str] | None = None,
        input_modes: list[str] | None = None,
        output_modes: list[str] | None = None,
    ) -> A2AAgentCard:
        return A2AAgentCard(
            name=name,
            skills=[A2ASkill(id=sid, name=sn) for sid, sn in (skills or [])],
            authentication=A2AAuthentication(schemes=auth_schemes or []),
            defaultInputModes=input_modes or ["text/plain"],
            defaultOutputModes=output_modes or ["text/plain"],
        )

    def test_compatible_with_shared_skills(self) -> None:
        local = self._make_card("Local", skills=[("s1", "Skill 1"), ("s2", "Skill 2")])
        remote = self._make_card("Remote", skills=[("s2", "Skill 2"), ("s3", "Skill 3")])
        result = negotiate(local, remote)
        assert result.compatible
        assert result.shared_skills == ["s2"]
        assert result.local_only == ["s1"]
        assert result.remote_only == ["s3"]

    def test_no_shared_skills_incompatible(self) -> None:
        local = self._make_card("Local", skills=[("s1", "Skill 1")])
        remote = self._make_card("Remote", skills=[("s2", "Skill 2")])
        result = negotiate(local, remote)
        assert not result.compatible
        assert result.shared_skills == []

    def test_auth_mismatch(self) -> None:
        local = self._make_card("Local", skills=[("s1", "S1")], auth_schemes=["api_key"])
        remote = self._make_card("Remote", skills=[("s1", "S1")], auth_schemes=["bearer"])
        result = negotiate(local, remote)
        assert not result.compatible
        assert not result.auth_compatible
        assert any("Auth mismatch" in n for n in result.notes)

    def test_auth_compatible(self) -> None:
        local = self._make_card("Local", skills=[("s1", "S1")], auth_schemes=["bearer"])
        remote = self._make_card("Remote", skills=[("s1", "S1")], auth_schemes=["bearer"])
        result = negotiate(local, remote)
        assert result.compatible
        assert result.auth_compatible

    def test_output_mode_mismatch_noted(self) -> None:
        local = self._make_card("Local", skills=[("s1", "S1")], input_modes=["text/plain"])
        remote = self._make_card("Remote", skills=[("s1", "S1")], output_modes=["application/pdf"])
        result = negotiate(local, remote)
        assert any("Output format mismatch" in n for n in result.notes)

    def test_empty_skills_both_sides(self) -> None:
        local = self._make_card("Local")
        remote = self._make_card("Remote")
        result = negotiate(local, remote)
        assert not result.compatible
        assert result.shared_skills == []

    def test_remote_no_auth_required(self) -> None:
        local = self._make_card("Local", skills=[("s1", "S1")])
        remote = self._make_card("Remote", skills=[("s1", "S1")])
        result = negotiate(local, remote)
        assert result.auth_compatible


# ── local_agent_card ─────────────────────────────────────────────────────────


class TestLocalAgentCard:
    def test_generates_valid_card(self, tmp_path: str) -> None:
        card = local_agent_card(str(tmp_path) if isinstance(tmp_path, type(None)) else ".")
        assert card.name == "ASS-ADE"
        assert card.provider is not None
        assert card.provider.organization == "Atomadic"
        assert len(card.skills) > 0

    def test_card_validates(self) -> None:
        card = local_agent_card(".")
        report = validate_agent_card(card.model_dump())
        # Should be valid (may have warnings but no errors)
        assert not report.errors


# ── Models ───────────────────────────────────────────────────────────────────


class TestModels:
    def test_agent_card_name_validation(self) -> None:
        with pytest.raises(Exception):
            A2AAgentCard(name="")

    def test_agent_card_with_payment(self) -> None:
        card = A2AAgentCard(name="Paid", payment={"type": "x402"})
        assert card.payment == {"type": "x402"}

    def test_validation_report_properties(self) -> None:
        issues = [
            ValidationIssue("error", "f1", "bad"),
            ValidationIssue("warning", "f2", "meh"),
            ValidationIssue("error", "f3", "also bad"),
        ]
        report = ValidationReport(valid=False, issues=issues)
        assert len(report.errors) == 2
        assert len(report.warnings) == 1
