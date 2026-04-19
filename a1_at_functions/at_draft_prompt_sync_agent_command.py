# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a1_at_functions/at_draft_prompt_sync_agent_command.py:7
# Component id: at.source.a1_at_functions.prompt_sync_agent_command
from __future__ import annotations

__version__ = "0.1.0"

def prompt_sync_agent_command(
    path: Path = REPO_PATH_OPTION,
    prompt_path: Path = typer.Option(
        Path("agents/atomadic_interpreter.md"),
        "--prompt-path",
        help="Prompt artifact to refresh, relative to --path unless absolute.",
    ),
    json_out: bool = typer.Option(False, "--json", help="Output raw JSON."),
) -> None:
    """Refresh Atomadic's generated capability block from live commands and tools."""
    from ass_ade.agent.capabilities import sync_atomadic_prompt_capabilities

    target = sync_atomadic_prompt_capabilities(repo_root=path, prompt_path=prompt_path)
    payload = {"path": str(target), "ok": True}
    if json_out:
        _print_json(payload)
    else:
        console.print(f"[green]Synced Atomadic capabilities:[/green] {target}")
