# Extracted from C:/!ass-ade/tests/test_capabilities.py:141
# Component id: at.source.ass_ade.fake_execute
from __future__ import annotations

__version__ = "0.1.0"

def fake_execute(self: Atomadic, cmd: list[str]) -> str:
    captured["cmd"] = cmd
    return '{"profile":"local"}'
