"""Tier a1 — assimilated function 'validate_blueprint'

Assimilated from: blueprint.py:104-115
"""

from __future__ import annotations


# --- assimilated symbol ---
def validate_blueprint(
    spec: Path = typer.Argument(..., help="Path to blueprint JSON."),
) -> None:
    """Validate a blueprint file against the minimum schema."""
    data = _load_blueprint(spec)
    problems = _validate_blueprint(data)
    if problems:
        _console.print(f"[red]invalid[/red] ({len(problems)} issue(s)):")
        for p in problems:
            _console.print(f"  - {p}")
        raise typer.Exit(code=1)
    _console.print(f"[green]valid[/green] ({data.get('schema', 'unknown schema')})")

