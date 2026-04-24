"""Tests for search command and x402 payment handling.

Tests cover:
- search command: requires session token, returns RAG results
- x402 payment client: parses 402 responses, extracts payment details
"""
from __future__ import annotations

import json
from pathlib import Path
from unittest.mock import MagicMock, patch

import httpx
import pytest
from typer.testing import CliRunner

from ass_ade.cli import app
from ass_ade.config import AssAdeConfig, write_default_config
from ass_ade.nexus.client import NexusClient
from ass_ade.nexus.errors import NexusPaymentRequired

runner = CliRunner()


def _hybrid_config(tmp_path: Path) -> Path:
    config_path = tmp_path / ".ass-ade" / "config.json"
    write_default_config(config_path, config=AssAdeConfig(profile="hybrid"), overwrite=True)
    return config_path


def _make_ctx_mgr(mock_instance: MagicMock) -> MagicMock:
    ctx = MagicMock()
    ctx.__enter__ = MagicMock(return_value=mock_instance)
    ctx.__exit__ = MagicMock(return_value=False)
    return ctx


# ---------------------------------------------------------------------------
# Search command tests
# ---------------------------------------------------------------------------


class TestSearchCommand:
    def test_search_requires_session_token(self, tmp_path: Path) -> None:
        """Search should fail if ATOMADIC_SESSION_TOKEN is not set."""
        result = runner.invoke(
            app,
            ["search", "test query", "--config", str(_hybrid_config(tmp_path))],
            env={"ATOMADIC_SESSION_TOKEN": ""},
        )
        assert result.exit_code == 1
        assert "ATOMADIC_SESSION_TOKEN" in result.stdout

    def test_search_calls_internal_search(self, tmp_path: Path) -> None:
        """Search with valid session token should call internal_search."""
        mock_nx = MagicMock()
        mock_nx.internal_search.return_value = {
            "success": True,
            "result": {"search_query": "test results", "chunks": []},
        }
        with patch("ass_ade.cli.NexusClient", return_value=_make_ctx_mgr(mock_nx)):
            result = runner.invoke(
                app,
                ["search", "Atomadic invariants", "--config", str(_hybrid_config(tmp_path))],
                env={"ATOMADIC_SESSION_TOKEN": "test-session-abc123"},
            )
        assert result.exit_code == 0
        mock_nx.internal_search.assert_called_once_with(
            query="Atomadic invariants",
            max_results=10,
            session_token="test-session-abc123",
        )

    def test_search_chat_mode(self, tmp_path: Path) -> None:
        """Search with --chat flag should call internal_search_chat."""
        mock_nx = MagicMock()
        mock_nx.internal_search_chat.return_value = {
            "success": True,
            "result": {"response": "The Atomadic codex defines..."},
        }
        with patch("ass_ade.cli.NexusClient", return_value=_make_ctx_mgr(mock_nx)):
            result = runner.invoke(
                app,
                ["search", "what is the codex", "--chat", "--config", str(_hybrid_config(tmp_path))],
                env={"ATOMADIC_SESSION_TOKEN": "test-session-abc123"},
            )
        assert result.exit_code == 0
        mock_nx.internal_search_chat.assert_called_once()

    def test_search_custom_max_results(self, tmp_path: Path) -> None:
        """Search with --max-results should pass through to client."""
        mock_nx = MagicMock()
        mock_nx.internal_search.return_value = {"success": True, "result": {}}
        with patch("ass_ade.cli.NexusClient", return_value=_make_ctx_mgr(mock_nx)):
            result = runner.invoke(
                app,
                ["search", "query", "--max-results", "5", "--config", str(_hybrid_config(tmp_path))],
                env={"ATOMADIC_SESSION_TOKEN": "sess-tok"},
            )
        assert result.exit_code == 0
        mock_nx.internal_search.assert_called_once_with(
            query="query", max_results=5, session_token="sess-tok"
        )


# ---------------------------------------------------------------------------
# x402 payment client tests
# ---------------------------------------------------------------------------


class TestX402PaymentHandling:
    def _make_client(self) -> NexusClient:
        transport = httpx.MockTransport(lambda req: httpx.Response(200, json={}))
        return NexusClient(base_url="https://test.atomadic.tech", transport=transport)

    def test_handle_x402_parses_payment_details(self) -> None:
        """handle_x402 should extract amount, network, treasury from 402 body."""
        client = self._make_client()
        mock_response = httpx.Response(
            402,
            json={
                "amount": 0.008,
                "network": "base",
                "address": "0xCBd9e4c44958ee76E0F941106Ea960D476c48FD9",
                "endpoint": "/v1/trust/score",
                "detail": "Payment required: $0.008 USDC",
            },
        )
        result = client.handle_x402(mock_response)
        assert result["payment_required"] is True
        assert result["amount_usdc"] == 0.008
        assert result["network"] == "base"
        assert result["treasury"] == "0xCBd9e4c44958ee76E0F941106Ea960D476c48FD9"
        assert result["endpoint"] == "/v1/trust/score"
        client.close()

    def test_handle_x402_fallback_fields(self) -> None:
        """handle_x402 should handle alternative field names."""
        client = self._make_client()
        mock_response = httpx.Response(
            402,
            json={
                "price_usdc": 0.04,
                "treasury": "0xABC123",
                "message": "Insufficient credits",
            },
        )
        result = client.handle_x402(mock_response)
        assert result["payment_required"] is True
        assert result["amount_usdc"] == 0.04
        assert result["treasury"] == "0xABC123"
        assert result["detail"] == "Insufficient credits"
        client.close()

    def test_handle_x402_empty_body(self) -> None:
        """handle_x402 should handle empty or malformed 402 body."""
        client = self._make_client()
        mock_response = httpx.Response(402, text="Payment Required")
        result = client.handle_x402(mock_response)
        assert result["payment_required"] is True
        assert result["amount_usdc"] == 0
        assert result["network"] == "base"
        client.close()

    def test_post_with_x402_returns_payment_on_402(self) -> None:
        """_post_with_x402 should return payment details instead of raising on 402."""
        def handler(request: httpx.Request) -> httpx.Response:
            return httpx.Response(
                402,
                json={"amount": 0.008, "network": "base", "address": "0xTREASURY"},
            )

        transport = httpx.MockTransport(handler)
        client = NexusClient(base_url="https://test.atomadic.tech", transport=transport)
        result = client._post_with_x402("/v1/trust/score", {"agent_id": "test"})
        assert result["payment_required"] is True
        assert result["amount_usdc"] == 0.008
        client.close()

    def test_post_with_x402_passes_through_on_200(self) -> None:
        """_post_with_x402 should return normal response on 200."""
        def handler(request: httpx.Request) -> httpx.Response:
            return httpx.Response(200, json={"trust_score": 0.95})

        transport = httpx.MockTransport(handler)
        client = NexusClient(base_url="https://test.atomadic.tech", transport=transport)
        result = client._post_with_x402("/v1/trust/score", {"agent_id": "test"})
        assert result == {"trust_score": 0.95}
        client.close()

    def test_post_with_x402_raises_on_other_errors(self) -> None:
        """_post_with_x402 should raise on non-402 errors (401, 500, etc.)."""
        def handler(request: httpx.Request) -> httpx.Response:
            return httpx.Response(401, json={"error": "unauthorized"})

        transport = httpx.MockTransport(handler)
        client = NexusClient(base_url="https://test.atomadic.tech", transport=transport)
        from ass_ade.nexus.errors import NexusAuthError
        with pytest.raises(NexusAuthError):
            client._post_with_x402("/v1/trust/score")
        client.close()


# ---------------------------------------------------------------------------
# NexusClient internal search tests
# ---------------------------------------------------------------------------


class TestNexusClientSearch:
    def test_internal_search_sends_session_token(self) -> None:
        """internal_search should include X-Owner-Token header."""
        requests_made = []

        def handler(request: httpx.Request) -> httpx.Response:
            requests_made.append(request)
            return httpx.Response(200, json={"success": True, "result": {}})

        transport = httpx.MockTransport(handler)
        client = NexusClient(base_url="https://test.atomadic.tech", transport=transport)
        client.internal_search("test query", session_token="my-session-123")
        assert len(requests_made) == 1
        assert requests_made[0].headers.get("X-Owner-Token") == "my-session-123"
        client.close()

    def test_internal_search_chat_sends_query(self) -> None:
        """internal_search_chat should POST to /internal/search/chat."""
        requests_made = []

        def handler(request: httpx.Request) -> httpx.Response:
            requests_made.append(request)
            return httpx.Response(200, json={"success": True, "result": {"response": "answer"}})

        transport = httpx.MockTransport(handler)
        client = NexusClient(base_url="https://test.atomadic.tech", transport=transport)
        result = client.internal_search_chat("what is codex", session_token="sess")
        assert result["success"] is True
        assert "/internal/search/chat" in str(requests_made[0].url)
        client.close()
