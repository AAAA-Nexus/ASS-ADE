# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a1_at_functions/at_draft_a2a_local_card.py:7
# Component id: at.source.a1_at_functions.a2a_local_card
from __future__ import annotations

__version__ = "0.1.0"

def a2a_local_card(
    working_dir: Path = typer.Option(
        Path("."), exists=True, file_okay=False, help="Working directory."
    ),
    json_out: bool = typer.Option(False, "--json", help="Output raw JSON."),
) -> None:
    """Display the local ASS-ADE agent card."""
    from ass_ade.a2a import local_agent_card

    card = local_agent_card(str(working_dir.resolve()))

    if json_out:
        _print_json(card.model_dump())
    else:
        console.print(f"[bold]{card.name}[/bold] v{card.version or '?'}")
        console.print(f"  {card.description}")
        if card.skills:
            console.print(f"\n[bold]Skills ({len(card.skills)}):[/bold]")
            for skill in card.skills:
                console.print(f"  • [cyan]{skill.id}[/cyan] — {skill.description}")
