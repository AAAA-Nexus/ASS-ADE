"""Model providers — OpenAI-compatible and Nexus inference."""

from __future__ import annotations

import json
import uuid
from collections.abc import Iterator
from typing import Any, Protocol, runtime_checkable

import httpx

from ass_ade.engine.types import (
    CompletionRequest,
    CompletionResponse,
    Message,
    ToolCallRequest,
)


@runtime_checkable
class ModelProvider(Protocol):
    """Protocol for LLM providers."""

    def complete(self, request: CompletionRequest) -> CompletionResponse: ...


class OpenAICompatibleProvider:
    """Calls any OpenAI-compatible chat/completions API.

    Works with: OpenAI, Ollama, LM Studio, vLLM, Together, Groq,
    Fireworks, DeepSeek, and any other OpenAI-compatible provider.
    """

    def __init__(
        self,
        *,
        base_url: str = "https://api.openai.com/v1",
        api_key: str = "",
        model: str = "gpt-4o",
        timeout: float = 120.0,
    ) -> None:
        headers: dict[str, str] = {"Content-Type": "application/json"}
        if api_key:
            headers["Authorization"] = f"Bearer {api_key}"
        self._client = httpx.Client(
            base_url=base_url.rstrip("/"),
            headers=headers,
            timeout=timeout,
        )
        self._default_model = model

    def close(self) -> None:
        self._client.close()

    @property
    def model_name(self) -> str:
        return self._default_model

    def complete(self, request: CompletionRequest) -> CompletionResponse:
        model = request.model or self._default_model
        body: dict[str, Any] = {
            "model": model,
            "messages": [self._format_message(m) for m in request.messages],
            "temperature": request.temperature,
            "max_tokens": request.max_tokens,
        }
        if request.tools:
            body["tools"] = [
                {
                    "type": "function",
                    "function": {
                        "name": t.name,
                        "description": t.description,
                        "parameters": t.parameters,
                    },
                }
                for t in request.tools
            ]

        resp = self._client.post("/chat/completions", json=body)
        resp.raise_for_status()
        data = resp.json()

        choice = data["choices"][0]
        msg_data = choice["message"]

        tool_calls: list[ToolCallRequest] = []
        if raw_calls := msg_data.get("tool_calls"):
            for tc in raw_calls:
                fn = tc["function"]
                try:
                    args = (
                        json.loads(fn["arguments"])
                        if isinstance(fn["arguments"], str)
                        else fn["arguments"]
                    )
                except json.JSONDecodeError:
                    args = {"raw": fn["arguments"]}
                tool_calls.append(
                    ToolCallRequest(
                        id=tc["id"],
                        name=fn["name"],
                        arguments=args,
                    )
                )

        message = Message(
            role="assistant",
            content=msg_data.get("content") or "",
            tool_calls=tool_calls,
        )

        return CompletionResponse(
            message=message,
            model=data.get("model"),
            finish_reason=choice.get("finish_reason"),
            usage=data.get("usage"),
        )

    def stream(self, request: CompletionRequest) -> Iterator[str]:
        """Streaming variant — yields text chunks."""
        model = request.model or self._default_model
        body: dict[str, Any] = {
            "model": model,
            "messages": [self._format_message(m) for m in request.messages],
            "temperature": request.temperature,
            "max_tokens": request.max_tokens,
            "stream": True,
        }
        with self._client.stream("POST", "/chat/completions", json=body) as resp:
            resp.raise_for_status()
            for line in resp.iter_lines():
                if not line or not line.startswith("data: "):
                    continue
                payload = line[6:]
                if payload.strip() == "[DONE]":
                    break
                try:
                    chunk = json.loads(payload)
                    delta = chunk["choices"][0].get("delta", {})
                    if text := delta.get("content"):
                        yield text
                except (json.JSONDecodeError, KeyError, IndexError):
                    continue

    @staticmethod
    def _format_message(msg: Message) -> dict[str, Any]:
        d: dict[str, Any] = {"role": msg.role, "content": msg.content}
        if msg.tool_calls:
            d["tool_calls"] = [
                {
                    "id": tc.id,
                    "type": "function",
                    "function": {
                        "name": tc.name,
                        "arguments": json.dumps(tc.arguments),
                    },
                }
                for tc in msg.tool_calls
            ]
        if msg.tool_call_id:
            d["tool_call_id"] = msg.tool_call_id
        if msg.name:
            d["name"] = msg.name
        return d


class AnthropicProvider:
    """Calls the Anthropic Messages API directly.

    Uses the native /v1/messages endpoint — NOT the OpenAI-compat shim,
    which does not exist on api.anthropic.com.
    """

    def __init__(
        self,
        *,
        api_key: str,
        model: str = "claude-sonnet-4-20250514",
        timeout: float = 120.0,
    ) -> None:
        self._client = httpx.Client(
            base_url="https://api.anthropic.com",
            headers={
                "x-api-key": api_key,
                "anthropic-version": "2023-06-01",
                "content-type": "application/json",
            },
            timeout=timeout,
        )
        self._default_model = model

    def close(self) -> None:
        self._client.close()

    @property
    def model_name(self) -> str:
        return self._default_model

    def complete(self, request: CompletionRequest) -> CompletionResponse:
        model = request.model or self._default_model

        # Split system message out — Anthropic requires it as a top-level field.
        system = ""
        messages: list[dict[str, Any]] = []
        for msg in request.messages:
            if msg.role == "system":
                system = msg.content
            elif msg.role == "tool":
                # Tool results use a user message with tool_result content blocks.
                messages.append({
                    "role": "user",
                    "content": [{
                        "type": "tool_result",
                        "tool_use_id": msg.tool_call_id or "",
                        "content": msg.content,
                    }],
                })
            elif msg.tool_calls:
                # Assistant turn that includes tool calls.
                content: list[dict[str, Any]] = []
                if msg.content:
                    content.append({"type": "text", "text": msg.content})
                for tc in msg.tool_calls:
                    content.append({
                        "type": "tool_use",
                        "id": tc.id,
                        "name": tc.name,
                        "input": tc.arguments,
                    })
                messages.append({"role": "assistant", "content": content})
            else:
                messages.append({"role": msg.role, "content": msg.content})

        body: dict[str, Any] = {
            "model": model,
            "max_tokens": request.max_tokens,
            "messages": messages,
        }
        if system:
            body["system"] = system
        if request.tools:
            body["tools"] = [
                {
                    "name": t.name,
                    "description": t.description,
                    "input_schema": t.parameters,
                }
                for t in request.tools
            ]

        resp = self._client.post("/v1/messages", json=body)
        resp.raise_for_status()
        data = resp.json()

        text_parts: list[str] = []
        tool_calls: list[ToolCallRequest] = []
        for block in data.get("content", []):
            if block.get("type") == "text":
                text_parts.append(block["text"])
            elif block.get("type") == "tool_use":
                tool_calls.append(ToolCallRequest(
                    id=block["id"],
                    name=block["name"],
                    arguments=block.get("input", {}),
                ))

        message = Message(
            role="assistant",
            content="".join(text_parts),
            tool_calls=tool_calls,
        )
        return CompletionResponse(
            message=message,
            model=data.get("model"),
            finish_reason=data.get("stop_reason"),
            usage=data.get("usage"),
        )


class MultiProvider:
    """Routes each CompletionRequest to the right underlying provider by model.

    Holds a dict of {provider_name: ModelProvider} and a reverse map from
    model id → provider_name. If the requested model is unknown, falls back
    to the first provider in fallback order. On HTTP/network errors, tries
    the next provider in the fallback chain.

    Used by the LSE-enabled AgentLoop: when LSE picks model X for step N,
    MultiProvider finds which underlying provider serves X and routes the call
    there. The next step can route to a completely different provider.
    """

    def __init__(
        self,
        providers: dict[str, "ModelProvider"],
        model_to_provider: dict[str, str] | None = None,
        fallback_order: list[str] | None = None,
    ) -> None:
        self._providers = dict(providers)
        self._model_to_provider = dict(model_to_provider or {})
        self._fallback_order = list(fallback_order or providers.keys())
        self._last_provider_name: str | None = None

    @property
    def providers(self) -> dict[str, "ModelProvider"]:
        return dict(self._providers)

    @property
    def last_provider_name(self) -> str | None:
        return self._last_provider_name

    @property
    def model_name(self) -> str:
        # For compatibility with the OpenAICompatibleProvider property
        if self._providers and self._fallback_order:
            first = self._providers.get(self._fallback_order[0])
            if first is not None and hasattr(first, "model_name"):
                return first.model_name  # type: ignore[no-any-return]
        return "multi-provider"

    def register(self, name: str, provider: "ModelProvider", models: list[str] | None = None) -> None:
        """Add a provider to the router at runtime."""
        self._providers[name] = provider
        if name not in self._fallback_order:
            self._fallback_order.append(name)
        for m in models or []:
            self._model_to_provider[m] = name

    def close(self) -> None:
        for p in self._providers.values():
            close = getattr(p, "close", None)
            if callable(close):
                try:
                    close()
                except Exception:
                    pass

    def complete(self, request: CompletionRequest) -> CompletionResponse:
        """Route a request to the right provider, with automatic fallback."""
        order = self._select_order(request.model)
        last_error: Exception | None = None
        for name in order:
            provider = self._providers.get(name)
            if provider is None:
                continue
            try:
                response = provider.complete(request)
                self._last_provider_name = name
                return response
            except httpx.HTTPError as exc:
                last_error = exc
                continue
            except Exception as exc:  # noqa: BLE001
                last_error = exc
                continue
        # All providers failed — re-raise the last error so the caller sees it.
        if last_error is not None:
            raise last_error
        raise RuntimeError("MultiProvider: no providers configured")

    def _select_order(self, model: str | None) -> list[str]:
        """Compute provider-try order for a given model."""
        if not model:
            return list(self._fallback_order)
        primary = self._model_to_provider.get(model)
        if primary is None:
            return list(self._fallback_order)
        order = [primary]
        order.extend(n for n in self._fallback_order if n != primary)
        return order


class NexusProvider:
    """Uses AAAA-Nexus /v1/inference as the model backend.

    Routes through the Nexus LLM endpoint. In premium mode, quality
    gates (hallucination oracle, epistemic routing) are applied
    server-side.
    """

    DEFAULT_MODEL = "gemma-4-26b-a4b-it"

    def __init__(self, client: Any) -> None:
        self._client = client

    @property
    def model_name(self) -> str:
        return self.DEFAULT_MODEL

    def complete(self, request: CompletionRequest) -> CompletionResponse:
        model = request.model or self.model_name
        prompt = self._messages_to_prompt(request.messages, request.tools)
        result = self._client.inference(prompt, model=model)

        text = result.result or result.text or ""

        # Parse tool calls from the response if tools were provided
        tool_calls, content = self._parse_tool_calls(text, request.tools)

        return CompletionResponse(
            message=Message(
                role="assistant",
                content=content,
                tool_calls=tool_calls,
            ),
            model=result.model or model,
            finish_reason="tool_calls" if tool_calls else "stop",
        )

    @staticmethod
    def _messages_to_prompt(messages: list[Message], tools: list[Any]) -> str:
        parts: list[str] = []
        for msg in messages:
            if msg.role == "system":
                parts.append(f"[System]\n{msg.content}")
            elif msg.role == "user":
                parts.append(f"[User]\n{msg.content}")
            elif msg.role == "assistant":
                parts.append(f"[Assistant]\n{msg.content}")
            elif msg.role == "tool":
                parts.append(f"[Tool Result: {msg.name}]\n{msg.content}")

        if tools:
            tool_desc = "\n".join(f"- {t.name}: {t.description}" for t in tools)
            parts.append(f"\nAvailable tools:\n{tool_desc}")
            parts.append(
                '\nTo call a tool, respond with exactly this JSON format: '
                '{"tool_call": {"name": "tool_name", "arguments": {...}}}'
            )

        return "\n\n".join(parts)

    @staticmethod
    def _parse_tool_calls(
        text: str, tools: list[Any]
    ) -> tuple[list[ToolCallRequest], str]:
        if not tools:
            return [], text

        # Try to extract a JSON tool call from the response
        try:
            data = json.loads(text.strip())
            if isinstance(data, dict) and "tool_call" in data:
                tc = data["tool_call"]
                return [
                    ToolCallRequest(
                        id=f"call_{uuid.uuid4().hex[:8]}",
                        name=tc["name"],
                        arguments=tc.get("arguments", {}),
                    )
                ], ""
        except (json.JSONDecodeError, KeyError, TypeError):
            pass

        return [], text
