# Extracted from C:/!ass-ade/tests/test_capabilities.py:69
# Component id: sy.source.ass_ade.test_llm_router_sends_dynamic_capability_prompt
from __future__ import annotations

__version__ = "0.1.0"

def test_llm_router_sends_dynamic_capability_prompt(monkeypatch, tmp_path: Path) -> None:
    captured: dict[str, object] = {}

    def fake_post(url: str, **kwargs):
        captured["url"] = url
        captured["json"] = kwargs["json"]
        response = MagicMock()
        response.json.return_value = {
            "choices": [
                {
                    "message": {
                        "content": (
                            '{"type":"command","intent":"help","path":null,'
                            '"output_path":null,"feature_desc":null}'
                        )
                    }
                }
            ]
        }
        response.raise_for_status.return_value = None
        return response

    monkeypatch.setattr(interpreter, "_pick_endpoint", lambda: ("https://llm.example/v1", "key", "model"))
    monkeypatch.setattr(interpreter.httpx, "post", fake_post)

    result = interpreter._call_llm(
        "what can you do?",
        working_dir=tmp_path,
        memory_context="preferred_tone=direct",
    )

    assert result and result["intent"] == "help"
    payload = captured["json"]
    assert isinstance(payload, dict)
    system_prompt = payload["messages"][0]["content"]
    assert "Dynamic Capability Inventory" in system_prompt
    assert "Runtime routing rules" in system_prompt
    assert "`mcp serve`" in system_prompt
    assert "preferred_tone=direct" in system_prompt
