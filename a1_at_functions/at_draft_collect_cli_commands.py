# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a1_at_functions/at_draft_collect_cli_commands.py:7
# Component id: at.source.a1_at_functions.collect_cli_commands
from __future__ import annotations

__version__ = "0.1.0"

def collect_cli_commands() -> list[CapabilityEntry]:
    """Return current CLI command paths by introspecting the Typer app."""
    try:
        click_root = _get_click_root()
        return _walk_click_command(click_root)
    except Exception:
        return []
