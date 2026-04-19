# Extracted from C:/!ass-ade/tests/test_capabilities.py:131
# Component id: at.source.ass_ade.fake_call_llm
from __future__ import annotations

__version__ = "0.1.0"

def fake_call_llm(_text: str, _working_dir: Path | str | None = None, _memory_context: str | None = None) -> dict:
    return {
        "type": "command",
        "intent": "cli",
        "cli_args": ["doctor", "--json"],
        "path": None,
        "output_path": None,
        "feature_desc": None,
    }
