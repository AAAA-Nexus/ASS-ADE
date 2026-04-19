# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a1_at_functions/at_draft_test_atomadic_dispatches_dynamic_cli_args.py:7
# Component id: at.source.a1_at_functions.test_atomadic_dispatches_dynamic_cli_args
from __future__ import annotations

__version__ = "0.1.0"

def test_atomadic_dispatches_dynamic_cli_args(monkeypatch, tmp_path: Path) -> None:
    captured: dict[str, list[str]] = {}

    def fake_call_llm(_text: str, _working_dir: Path | str | None = None) -> dict:
        return {
            "type": "command",
            "intent": "cli",
            "cli_args": ["doctor", "--json"],
            "path": None,
            "output_path": None,
            "feature_desc": None,
        }

    def fake_execute(self: Atomadic, cmd: list[str]) -> str:
        captured["cmd"] = cmd
        return '{"profile":"local"}'

    monkeypatch.setattr(interpreter, "_call_llm", fake_call_llm)
    monkeypatch.setattr(Atomadic, "_execute", fake_execute)

    agent = Atomadic(working_dir=tmp_path)
    response = agent.process("show doctor json")

    assert captured["cmd"][-2:] == ["doctor", "--json"]
    assert "Command complete" in response
