"""Tier a1 — assimilated function 'list_blueprints'

Assimilated from: blueprint.py:70-100
"""

from __future__ import annotations


# --- assimilated symbol ---
def list_blueprints(
    directory: Path = typer.Option(
        None,
        "--dir",
        "-d",
        help="Directory to scan. Defaults to $ASS_ADE_BLUEPRINTS_DIR or ./blueprints.",
    ),
) -> None:
    """List blueprint files found under the blueprints directory."""
    target = directory or _resolve_blueprints_dir()
    if not target.is_dir():
        _console.print(f"[yellow]no blueprints directory at {target}[/yellow]")
        raise typer.Exit(code=0)
    matches = sorted(target.glob("blueprint*.json"))
    if not matches:
        _console.print(f"[yellow]no blueprints in {target}[/yellow]")
        raise typer.Exit(code=0)
    table = Table(title=f"Blueprints in {target}")
    table.add_column("file", style="cyan")
    table.add_column("description")
    table.add_column("components", justify="right")
    for path in matches:
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            table.add_row(path.name, "[red]invalid JSON[/red]", "-")
            continue
        desc = str(data.get("description", ""))[:60]
        comps = data.get("components") or []
        table.add_row(path.name, desc, str(len(comps)))
    _console.print(table)

