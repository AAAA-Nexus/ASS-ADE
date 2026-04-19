# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a1_at_functions/at_draft_providers_enable.py:7
# Component id: at.source.a1_at_functions.providers_enable
from __future__ import annotations

__version__ = "0.1.0"

def providers_enable(
    name: Annotated[str, typer.Argument(help="Provider name to enable.")],
    config: Path | None = CONFIG_OPTION,
) -> None:
    """Enable a provider (include it in the fallback chain)."""
    _set_enabled(name, True, config)
