# Extracted from C:/!ass-ade/src/ass_ade/engine/provider.py:374
# Component id: mo.source.ass_ade.nexusprovider
from __future__ import annotations

__version__ = "0.1.0"

class NexusProvider:
    """Uses AAAA-Nexus /v1/inference as the model backend.

    Routes through the Nexus LLM endpoint. In premium mode, quality
    gates (hallucination oracle, epistemic routing) are applied
    server-side.
    """

    def __init__(self, client: Any) -> None:
        self._client = client

    @property
    def model_name(self) -> str:
        return "nexus-inference"

    def complete(self, request: CompletionRequest) -> CompletionResponse:
        prompt = self._messages_to_prompt(request.messages, request.tools)
        result = self._client.inference(prompt)

        text = result.result or result.text or ""

        # Parse tool calls from the response if tools were provided
        tool_calls, content = self._parse_tool_calls(text, request.tools)

        return CompletionResponse(
            message=Message(
                role="assistant",
                content=content,
                tool_calls=tool_calls,
            ),
            model=result.model or "nexus-inference",
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
