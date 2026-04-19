# Extracted from C:/!ass-ade/src/ass_ade/cli.py:5746
# Component id: at.source.ass_ade.rollback_command
from __future__ import annotations

__version__ = "0.1.0"

def rollback_command(
    path: Path = typer.Argument(Path("."), help="Project root to roll back (default: current directory)."),
    yes: bool = typer.Option(False, "--yes", "-y", help="Skip confirmation prompt."),
    json_out: bool = typer.Option(False, "--json", help="Print result as JSON."),
) -> None:
    """Restore the most recent backup created by a previous rebuild.

    Finds the newest folder matching ``*-backup-*`` next to the project root,
    shows what will be restored, asks for confirmation, then replaces the
    current project folder with the backup.

    Examples:
        ass-ade rollback .
        ass-ade rollback ./myproject --yes
    """
    import shutil as _shutil
    import stat as _stat

    target = path.resolve()
    if not target.exists():
        console.print(f"[red]Path does not exist:[/red] {target}")
        raise typer.Exit(code=1)

    parent = target.parent
    # On Windows, Path("C:") is not the drive root — ensure we use Path("C:/")
    # so that glob() searches the actual drive root directory.
    if str(parent) == parent.drive:
        parent = Path(parent.drive + "/")
    pattern = f"{target.name}-backup-*"
    candidates = sorted(
        [d for d in parent.glob(pattern) if d.is_dir()],
        key=lambda d: d.name,
        reverse=True,
    )

    if not candidates:
        msg = f"No backup folders found matching '{pattern}' in {parent}"
        if json_out:
            print(json.dumps({"ok": False, "error": msg}, indent=2))
        else:
            console.print(f"[yellow]{msg}[/yellow]")
        raise typer.Exit(code=1)

    backup = candidates[0]
    backup_files = sum(1 for f in backup.rglob("*") if f.is_file())
    current_files = sum(1 for f in target.rglob("*") if f.is_file())

    restore_info = {
        "target": str(target),
        "backup": str(backup),
        "backup_name": backup.name,
        "backup_files": backup_files,
        "current_files": current_files,
        "other_backups": [str(c) for c in candidates[1:5]],
    }

    if not yes and not json_out:
        console.print(f"[bold]Rollback plan:[/bold]")
        console.print(f"  Restore from : [cyan]{backup.name}[/cyan] ({backup_files} files)")
        console.print(f"  Overwrites   : [yellow]{target.name}[/yellow] ({current_files} files)")
        if len(candidates) > 1:
            console.print(f"  Other backups: {', '.join(c.name for c in candidates[1:4])}")
        confirmed = typer.confirm("Proceed with rollback?", default=False)
        if not confirmed:
            console.print("[dim]Rollback cancelled.[/dim]")
            raise typer.Exit(code=0)

    # Perform rollback
    def _on_rm_error(func, path, exc_info):
        os.chmod(path, _stat.S_IWRITE)
        func(path)

    try:
        if target.exists():
            _shutil.rmtree(str(target), onerror=_on_rm_error)
        _shutil.copytree(str(backup), str(target))
    except Exception as exc:
        if json_out:
            print(json.dumps({"ok": False, "error": str(exc), **restore_info}, indent=2))
        else:
            console.print(f"[red]Rollback failed:[/red] {exc}")
        raise typer.Exit(code=1)

    if json_out:
        print(json.dumps({"ok": True, **restore_info}, indent=2))
    else:
        console.print(f"[green][OK][/green] Rolled back to [bold]{backup.name}[/bold]")
        console.print(f"[dim]Restored {backup_files} files → {target}[/dim]")
