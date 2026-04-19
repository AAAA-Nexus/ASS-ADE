# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a2_mo_composites/mo_draft_testnexusprovider.py:7
# Component id: mo.source.a2_mo_composites.testnexusprovider
from __future__ import annotations

__version__ = "0.1.0"

class TestNexusProvider:
    def test_complete_text_response(self):
        mock_client = MagicMock()
        mock_client.inference.return_value = MagicMock(
            result="Hello from Nexus!",
            text=None,
            model="llama-3.1-8b",
        )

        provider = NexusProvider(mock_client)
        req = CompletionRequest(messages=[Message(role="user", content="hi")])
        resp = provider.complete(req)

        assert resp.message.content == "Hello from Nexus!"
        assert resp.model == "llama-3.1-8b"
        assert resp.finish_reason == "stop"

    def test_complete_tool_call_response(self):
        tool_json = json.dumps({"tool_call": {"name": "read_file", "arguments": {"path": "x.py"}}})
        mock_client = MagicMock()
        mock_client.inference.return_value = MagicMock(
            result=tool_json,
            text=None,
            model="llama-3.1-8b",
        )

        provider = NexusProvider(mock_client)
        req = CompletionRequest(
            messages=[Message(role="user", content="read x.py")],
            tools=[ToolSchema(name="read_file", description="Read file", parameters={"type": "object"})],
        )
        resp = provider.complete(req)

        assert len(resp.message.tool_calls) == 1
        assert resp.message.tool_calls[0].name == "read_file"
        assert resp.finish_reason == "tool_calls"
