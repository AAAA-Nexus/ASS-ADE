# Extracted from C:/!ass-ade/src/ass_ade/engine/provider.py:27
# Component id: mo.source.ass_ade.openaicompatibleprovider
from __future__ import annotations

__version__ = "0.1.0"

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
