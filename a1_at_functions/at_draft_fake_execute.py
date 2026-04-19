# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a1_at_functions/at_draft_test_atomadic_dispatches_dynamic_cli_args.py:20
# Component id: at.source.a1_at_functions.fake_execute
from __future__ import annotations

__version__ = "0.1.0"

def fake_execute(self: Atomadic, cmd: list[str]) -> str:
    captured["cmd"] = cmd
    return '{"profile":"local"}'
