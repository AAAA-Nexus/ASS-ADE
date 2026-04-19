# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a1_at_functions/at_draft_test_atomadic_dispatches_dynamic_cli_args.py:10
# Component id: at.source.a1_at_functions.fake_call_llm
from __future__ import annotations

__version__ = "0.1.0"

def fake_call_llm(_text: str, _working_dir: Path | str | None = None) -> dict:
    return {
        "type": "command",
        "intent": "cli",
        "cli_args": ["doctor", "--json"],
        "path": None,
        "output_path": None,
        "feature_desc": None,
    }
