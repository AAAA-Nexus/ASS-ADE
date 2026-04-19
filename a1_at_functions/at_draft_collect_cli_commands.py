# Extracted from C:/!ass-ade/src/ass_ade/agent/capabilities.py:80
# Component id: at.source.ass_ade.collect_cli_commands
from __future__ import annotations

__version__ = "0.1.0"

def collect_cli_commands() -> list[CapabilityEntry]:
    """Return current CLI command paths by introspecting the Typer app."""
    try:
        click_root = _get_click_root()
        return _walk_click_command(click_root)
    except Exception:
        return []
