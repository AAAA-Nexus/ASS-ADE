"""Tests for the ASS-ADE multi-model engine: types, provider, router."""

from __future__ import annotations

import json
from unittest.mock import MagicMock, patch

from ass_ade.engine.provider import (
    NexusProvider,
    OpenAICompatibleProvider,
)
from ass_ade.engine.router import build_provider
from ass_ade.engine.types import (
    CompletionRequest,
    CompletionResponse,
    Message,
    ToolCallRequest,
    ToolSchema,
)

# ── Types ─────────────────────────────────────────────────────────────────────


class TestMessage:
    def test_minimal(self):
        m = Message(role="user", content="hello")
        assert m.role == "user"
        assert m.content == "hello"
        assert m.tool_calls == []
        assert m.tool_call_id is None

    def test_with_tool_calls(self):
        tc = ToolCallRequest(id="c1", name="read_file", arguments={"path": "a.py"})
        m = Message(role="assistant", content="", tool_calls=[tc])
        assert len(m.tool_calls) == 1
        assert m.tool_calls[0].name == "read_file"

    def test_tool_result(self):
        m = Message(role="tool", content="file data", tool_call_id="c1", name="read_file")
        assert m.role == "tool"
        assert m.tool_call_id == "c1"


class TestToolSchema:
    def test_schema(self):
        s = ToolSchema(name="read_file", description="Read a file", parameters={"type": "object"})
        assert s.name == "read_file"


class TestCompletionRequest:
    def test_defaults(self):
        r = CompletionRequest(messages=[Message(role="user", content="hi")])
        assert r.temperature == 0.0
        assert r.max_tokens == 4096
        assert r.tools == []
        assert r.model is None


class TestCompletionResponse:
    def test_basic(self):
        r = CompletionResponse(
            message=Message(role="assistant", content="done"),
            finish_reason="stop",
        )
        assert r.finish_reason == "stop"
        assert r.model is None


# ── OpenAICompatibleProvider ──────────────────────────────────────────────────


class TestOpenAICompatibleProvider:
    def _mock_response(self, content="OK", tool_calls=None):
        """Build a mock httpx response for chat/completions."""
        msg: dict = {"role": "assistant", "content": content}
        if tool_calls:
            msg["tool_calls"] = tool_calls
        return {
            "choices": [{"message": msg, "finish_reason": "stop"}],
            "model": "test-model",
            "usage": {"prompt_tokens": 10, "completion_tokens": 5},
        }

    @patch("ass_ade.engine.provider.httpx.Client")
    def test_complete_basic(self, mock_client_cls):
        mock_resp = MagicMock()
        mock_resp.json.return_value = self._mock_response("Hello!")
        mock_resp.raise_for_status = MagicMock()

        mock_instance = MagicMock()
        mock_instance.post.return_value = mock_resp
        mock_client_cls.return_value = mock_instance

        provider = OpenAICompatibleProvider(base_url="http://test:8000/v1", api_key="k")
        req = CompletionRequest(messages=[Message(role="user", content="hi")])
        resp = provider.complete(req)

        assert resp.message.content == "Hello!"
        assert resp.finish_reason == "stop"
        assert resp.model == "test-model"

    @patch("ass_ade.engine.provider.httpx.Client")
    def test_complete_with_tool_calls(self, mock_client_cls):
        raw_tool_calls = [
            {
                "id": "call_1",
                "type": "function",
                "function": {
                    "name": "read_file",
                    "arguments": json.dumps({"path": "main.py"}),
                },
            }
        ]
        mock_resp = MagicMock()
        mock_resp.json.return_value = self._mock_response(content="", tool_calls=raw_tool_calls)
        mock_resp.raise_for_status = MagicMock()

        mock_instance = MagicMock()
        mock_instance.post.return_value = mock_resp
        mock_client_cls.return_value = mock_instance

        provider = OpenAICompatibleProvider(base_url="http://test:8000/v1", api_key="k")
        req = CompletionRequest(
            messages=[Message(role="user", content="read main.py")],
            tools=[ToolSchema(name="read_file", description="Read file", parameters={"type": "object"})],
        )
        resp = provider.complete(req)

        assert len(resp.message.tool_calls) == 1
        assert resp.message.tool_calls[0].name == "read_file"
        assert resp.message.tool_calls[0].arguments == {"path": "main.py"}


# ── NexusProvider ─────────────────────────────────────────────────────────────


class TestNexusProvider:
    def test_complete_text_response(self):
        mock_client = MagicMock()
        mock_client.inference.return_value = MagicMock(
            result="Hello from Nexus!",
            text=None,
            model="falcon3-10B-1.58",
        )

        provider = NexusProvider(mock_client)
        req = CompletionRequest(messages=[Message(role="user", content="hi")])
        resp = provider.complete(req)

        assert resp.message.content == "Hello from Nexus!"
        assert resp.model == "falcon3-10B-1.58"
        assert resp.finish_reason == "stop"
        mock_client.inference.assert_called_once_with("[User]\nhi", model="falcon3-10B-1.58")

    def test_complete_tool_call_response(self):
        tool_json = json.dumps({"tool_call": {"name": "read_file", "arguments": {"path": "x.py"}}})
        mock_client = MagicMock()
        mock_client.inference.return_value = MagicMock(
            result=tool_json,
            text=None,
            model="llama3-8B-1.58-100B",
        )

        provider = NexusProvider(mock_client)
        req = CompletionRequest(
            messages=[Message(role="user", content="read x.py")],
            tools=[ToolSchema(name="read_file", description="Read file", parameters={"type": "object"})],
            model="llama3-8B-1.58-100B",
        )
        resp = provider.complete(req)

        assert len(resp.message.tool_calls) == 1
        assert resp.message.tool_calls[0].name == "read_file"
        assert resp.finish_reason == "tool_calls"
        call_args, call_kwargs = mock_client.inference.call_args
        assert call_kwargs["model"] == "llama3-8B-1.58-100B"
        assert "[User]\nread x.py" in call_args[0]
        assert "Available tools" in call_args[0]


# ── Router ────────────────────────────────────────────────────────────────────


class TestBuildProvider:
    def _clear_provider_env(self) -> None:
        """Remove every provider env var so the test state is deterministic."""
        import os
        from ass_ade.agent.providers import FREE_PROVIDERS
        for key in ("OPENAI_API_KEY", "ANTHROPIC_API_KEY", "ASS_ADE_PROVIDER_URL"):
            os.environ.pop(key, None)
        for p in FREE_PROVIDERS.values():
            if p.api_key_env:
                os.environ.pop(p.api_key_env, None)

    def _disable_all_catalog(self, cfg, *, keep: tuple[str, ...] = ()):
        """Disable every catalog provider so the test isolates a single backend.

        `keep` is a tuple of names to leave enabled (e.g., ('nexus',) to test
        a Nexus-only setup).
        """
        from ass_ade.agent.providers import FREE_PROVIDERS
        from ass_ade.config import ProviderOverride
        for name in FREE_PROVIDERS:
            if name in keep:
                continue
            cfg.providers[name] = ProviderOverride(enabled=False)
        return cfg

    def test_openai_key_picks_openai(self, monkeypatch):
        self._clear_provider_env()
        monkeypatch.setenv("OPENAI_API_KEY", "sk-test")

        from ass_ade.config import AssAdeConfig
        from ass_ade.engine.provider import MultiProvider

        cfg = self._disable_all_catalog(AssAdeConfig(profile="local"))
        provider = build_provider(cfg)
        # With catalog disabled and only OPENAI_API_KEY set, should get a single provider
        assert isinstance(provider, OpenAICompatibleProvider)

    def test_openai_key_multiprovider_when_catalog_enabled(self, monkeypatch):
        """With catalog providers AND OpenAI key, build_provider returns MultiProvider."""
        self._clear_provider_env()
        monkeypatch.setenv("OPENAI_API_KEY", "sk-test")
        monkeypatch.setenv("GROQ_API_KEY", "sk-groq")

        from ass_ade.config import AssAdeConfig
        from ass_ade.engine.provider import MultiProvider

        cfg = AssAdeConfig(profile="local")
        provider = build_provider(cfg)
        assert isinstance(provider, MultiProvider)
        assert "openai" in provider.providers
        assert "groq" in provider.providers

    def test_fallback_to_ollama(self, monkeypatch):
        """With no keys and all catalog providers disabled, falls back to Ollama."""
        self._clear_provider_env()

        from ass_ade.config import AssAdeConfig

        cfg = self._disable_all_catalog(AssAdeConfig(profile="local"))
        provider = build_provider(cfg)
        assert isinstance(provider, OpenAICompatibleProvider)

    def test_nexus_provider_for_premium(self, monkeypatch):
        self._clear_provider_env()
        monkeypatch.setenv("AAAA_NEXUS_API_KEY", "an_test_key")

        from ass_ade.config import AssAdeConfig

        cfg = self._disable_all_catalog(
            AssAdeConfig(
                profile="premium",
                nexus_api_key="an_test_key",
                nexus_base_url="https://atomadic.tech",
            ),
            keep=("nexus",),  # leave Nexus enabled
        )
        provider = build_provider(cfg)
        # Only Nexus enabled → single return
        assert isinstance(provider, NexusProvider)

    def test_nexus_added_to_multiprovider_when_catalog_keys_present(self, monkeypatch):
        """Premium profile + catalog keys → MultiProvider containing nexus + free providers."""
        self._clear_provider_env()
        monkeypatch.setenv("GROQ_API_KEY", "sk-groq")
        monkeypatch.setenv("AAAA_NEXUS_API_KEY", "an_test_key")

        from ass_ade.config import AssAdeConfig
        from ass_ade.engine.provider import MultiProvider

        cfg = AssAdeConfig(
            profile="premium",
            nexus_api_key="an_test_key",
            nexus_base_url="https://atomadic.tech",
        )
        provider = build_provider(cfg)
        assert isinstance(provider, MultiProvider)
        assert "nexus" in provider.providers
        assert "groq" in provider.providers
