# Extracted from C:/!ass-ade/src/ass_ade/commands/providers.py:240
# Component id: at.source.ass_ade.providers_enable
from __future__ import annotations

__version__ = "0.1.0"

def providers_enable(
    name: Annotated[str, typer.Argument(help="Provider name to enable.")],
    config: Path | None = CONFIG_OPTION,
) -> None:
    """Enable a provider (include it in the fallback chain)."""
    _set_enabled(name, True, config)
