# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a1_at_functions/at_draft_providers_set_chain.py:7
# Component id: at.source.a1_at_functions.providers_set_chain
from __future__ import annotations

__version__ = "0.1.0"

def providers_set_chain(
    chain: Annotated[str, typer.Argument(help="Comma-separated provider names (e.g., 'groq,gemini,ollama').")],
    config: Path | None = CONFIG_OPTION,
) -> None:
    """Override the provider fallback chain."""
    target, settings = _resolve_config(config)
    names = [n.strip() for n in chain.split(",") if n.strip()]
    invalid = [n for n in names if get_provider(n) is None]
    if invalid:
        console.print(f"[red]Unknown providers:[/red] {', '.join(invalid)}")
        raise typer.Exit(code=1)
    settings.provider_fallback_chain = names
    _save_config(target, settings)
    console.print(f"[green]✓[/green] Fallback chain: {' → '.join(names)}")
