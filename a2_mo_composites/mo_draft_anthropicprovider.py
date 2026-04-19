# Extracted from C:/!ass-ade/src/ass_ade/engine/provider.py:168
# Component id: mo.source.ass_ade.anthropicprovider
from __future__ import annotations

__version__ = "0.1.0"

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
