"""Tests for A2A CLI commands.

Tests are aligned with the actual CLI implementations:
- a2a validate: validates a local agent card JSON file
- a2a discover: searches for agents by capability via NexusClient
- a2a negotiate: fetches remote agent card and runs local A2A negotiation
- a2a local-card: displays the local ASS-ADE agent card
"""

from __future__ import annotations

import json
from pathlib import Path
from unittest.mock import MagicMock, patch

from typer.testing import CliRunner

from ass_ade.cli import app
from ass_ade.config import AssAdeConfig, write_default_config
from ass_ade.nexus.models import (
    DiscoveryResult,
    DiscoveredAgent,
)

runner = CliRunner()


def _hybrid_config(tmp_path: Path) -> Path:
    config_path = tmp_path / ".ass-ade" / "config.json"
    write_default_config(config_path, config=AssAdeConfig(profile="hybrid"), overwrite=True)
    return config_path


def _make_ctx_mgr(mock_client: MagicMock) -> MagicMock:
    mgr = MagicMock()
    mgr.__enter__ = MagicMock(return_value=mock_client)
    mgr.__exit__ = MagicMock(return_value=False)
    return mgr


class TestA2AValidateCLI:
    def test_validate_valid_card(self, tmp_path: Path) -> None:
        card_file = tmp_path / "agent.json"
        card_file.write_text(json.dumps({
            "name": "TestAgent",
            "description": "A test agent",
            "url": "https://test.com",
            "version": "1.0.0",
            "skills": [{"id": "skill1", "name": "Test Skill"}],
        }), encoding="utf-8")

        result = runner.invoke(app, ["a2a", "validate", str(card_file)])
        assert result.exit_code == 0
        assert "Valid" in result.stdout or "TestAgent" in result.stdout

    def test_validate_missing_fields(self, tmp_path: Path) -> None:
        card_file = tmp_path / "bad.json"
        card_file.write_text(json.dumps({"description": "Missing name"}), encoding="utf-8")

        result = runner.invoke(app, ["a2a", "validate", str(card_file)])
        assert result.exit_code == 1

    def test_validate_missing_file(self) -> None:
        result = runner.invoke(app, ["a2a", "validate", "/nonexistent/agent.json"])
        assert result.exit_code == 1


class TestA2ADiscoverCLI:
    def test_discover_success(self, tmp_path: Path) -> None:
        mock_nx = MagicMock()
        mock_nx.discovery_search.return_value = DiscoveryResult(
            agents=[DiscoveredAgent(agent_id="agent-1", name="DiscoverMe")],
            total=1,
            query="search",
        )
        with patch("ass_ade.commands.a2a.NexusClient", return_value=_make_ctx_mgr(mock_nx)):
            result = runner.invoke(
                app, ["a2a", "discover", "search",
                       "--config", str(_hybrid_config(tmp_path)), "--allow-remote"]
            )
        assert result.exit_code == 0
        assert "DiscoverMe" in result.stdout

    def test_discover_requires_remote(self, tmp_path: Path) -> None:
        config_path = tmp_path / ".ass-ade" / "config.json"
        write_default_config(config_path, config=AssAdeConfig(profile="local"), overwrite=True)
        result = runner.invoke(app, ["a2a", "discover", "search", "--config", str(config_path)])
        assert result.exit_code == 2
        assert "disabled in the local profile" in result.stdout


class TestA2ANegotiateCLI:
    def test_negotiate_blocks_private_url(self, tmp_path: Path) -> None:
        result = runner.invoke(
            app, ["a2a", "negotiate", "http://192.168.1.1/.well-known/agent.json",
                   "--config", str(_hybrid_config(tmp_path))]
        )
        assert result.exit_code == 1
        assert "Blocked" in result.stdout

    def test_negotiate_invalid_remote_card(self, tmp_path: Path) -> None:
        mock_report = MagicMock()
        mock_report.valid = False
        mock_report.errors = [MagicMock(message="Missing name")]
        with patch("ass_ade.commands.a2a.fetch_agent_card", return_value=mock_report):
            result = runner.invoke(
                app, ["a2a", "negotiate", "https://example.com/.well-known/agent.json",
                       "--config", str(_hybrid_config(tmp_path))]
            )
        assert result.exit_code == 1

    def test_negotiate_success(self, tmp_path: Path) -> None:
        from ass_ade.a2a import A2AAgentCard, NegotiationResult
        remote_card = A2AAgentCard(
            name="RemoteAgent", description="A remote agent",
            url="https://example.com", version="1.0.0",
            skills=[], defaultInputModes=["text"], defaultOutputModes=["text"],
        )
        mock_report = MagicMock()
        mock_report.valid = True
        mock_report.card = remote_card

        neg_result = NegotiationResult(
            compatible=True, shared_skills=[], local_only=["read_file"],
            remote_only=[], auth_compatible=True, notes=[],
        )
        with patch("ass_ade.commands.a2a.fetch_agent_card", return_value=mock_report), \
             patch("ass_ade.commands.a2a.negotiate", return_value=neg_result), \
             patch("ass_ade.commands.a2a.local_agent_card", return_value=remote_card):
            result = runner.invoke(
                app, ["a2a", "negotiate", "https://example.com/.well-known/agent.json",
                       "--config", str(_hybrid_config(tmp_path))]
            )
        assert result.exit_code == 0
        data = json.loads(result.stdout)
        assert data["compatible"] is True


class TestA2ALocalCardCLI:
    def test_local_card_displays(self) -> None:
        result = runner.invoke(app, ["a2a", "local-card"])
        assert result.exit_code == 0
        assert "ASS-ADE" in result.stdout

    def test_local_card_json(self) -> None:
        result = runner.invoke(app, ["a2a", "local-card", "--json"])
        assert result.exit_code == 0
        data = json.loads(result.stdout, strict=False)
        assert data["name"] == "ASS-ADE"
        assert "skills" in data
