# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a1_at_functions/at_draft_command_path_exists.py:7
# Component id: at.source.a1_at_functions.command_path_exists
from __future__ import annotations

__version__ = "0.1.0"

def command_path_exists(args: list[str], working_dir: str | Path = ".") -> bool:
    """Return True if args starts with a known CLI command path."""
    if not args:
        return False
    tokens = [str(item).strip() for item in args if str(item).strip()]
    if not tokens:
        return False
    try:
        command = _get_click_root()
    except Exception:
        snapshot = build_capability_snapshot(working_dir)
        return " ".join(tokens[:1]) in snapshot.cli_paths

    matched = 0
    while matched < len(tokens):
        commands = getattr(command, "commands", None)
        if not isinstance(commands, dict):
            break
        next_token = tokens[matched]
        if next_token not in commands:
            break
        command = commands[next_token]
        matched += 1

    if matched == 0:
        return False
    if matched == len(tokens):
        return True

    # A group with subcommands should not accept an unknown subcommand token.
    remaining = tokens[matched:]
    if getattr(command, "commands", None) and remaining and not remaining[0].startswith("-"):
        return False
    return True
