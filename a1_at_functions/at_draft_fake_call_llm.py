# Extracted from C:/!ass-ade/.claude/worktrees/adoring-boyd-0e3a8f/tests/test_capabilities.py:74
# Component id: at.source.ass_ade.fake_call_llm
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
