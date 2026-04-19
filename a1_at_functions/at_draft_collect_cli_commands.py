# Extracted from C:/!ass-ade/.claude/worktrees/beautiful-dubinsky-c2cb48/a1_at_functions/at_draft_collect_cli_commands.py:5
# Component id: at.source.ass_ade.collect_cli_commands
__version__ = "0.1.0"

def collect_cli_commands() -> list[CapabilityEntry]:
    """Return current CLI command paths by introspecting the Typer app."""
    try:
        click_root = _get_click_root()
        return _walk_click_command(click_root)
    except Exception:
        return []
