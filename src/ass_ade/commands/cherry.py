"""Tier a4 — `ass-ade cherry-pick` command: interactive or scripted candidate selection after scouting."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Annotated, Optional

import typer
from rich.console import Console

console = Console()
_DEFAULT_TARGET = Path(".")


def cherry_pick_command(
    source: Annotated[
        Path,
        typer.Argument(
            exists=True,
            resolve_path=True,
            help=(
                "Scout report JSON (from ass-ade scout --json-out) "
                "OR a repository/folder to scan directly."
            ),
        ),
    ],
    target: Annotated[
        Path,
        typer.Option(
            "--target",
            "-t",
            file_okay=False,
            dir_okay=True,
            resolve_path=True,
            help="Project root where assimilated code will land. Defaults to current directory.",
        ),
    ] = _DEFAULT_TARGET,
    pick: Annotated[
        Optional[str],
        typer.Option(
            "--pick",
            "-p",
            help=(
                "Non-interactive selection: item numbers ('1,3,5-8'), "
                "'all', or action name ('assimilate', 'rebuild', 'enhance')."
            ),
        ),
    ] = None,
    action: Annotated[
        Optional[str],
        typer.Option(
            "--action",
            "-a",
            help="Pre-filter candidates by action before showing the menu (assimilate|rebuild|enhance|all).",
        ),
    ] = None,
    interactive: Annotated[
        bool,
        typer.Option(
            "--interactive/--no-interactive",
            help="Show menu and wait for stdin selection. Default: True unless --pick is set.",
        ),
    ] = True,
    out: Annotated[
        Optional[Path],
        typer.Option(
            "--out",
            "-o",
            file_okay=True,
            dir_okay=False,
            help="Override manifest output path. Default: <target>/.ass-ade/cherry_pick.json",
        ),
    ] = None,
    print_json: Annotated[
        bool,
        typer.Option("--json", help="Print the saved manifest or preview JSON to stdout."),
    ] = False,
    preview: Annotated[
        bool,
        typer.Option(
            "--preview",
            help="Show a preview of candidates without saving a manifest.",
        ),
    ] = False,
    min_confidence: Annotated[
        Optional[float],
        typer.Option(
            "--min-confidence",
            help="Drop candidates below this confidence threshold (0.0–1.0).",
        ),
    ] = None,
    quiet: Annotated[
        bool,
        typer.Option(
            "--quiet",
            "-q",
            help="Suppress console status output.",
        ),
    ] = False,
) -> None:
    """Scout a codebase and cherry-pick symbols to assimilate.

    Accepts either a scout JSON report (from `ass-ade scout --json-out`) or a directory
    to scan directly.  Presents a ranked, numbered menu of candidate functions, classes,
    and methods.  You select items interactively or via --pick.  The result is saved as a
    cherry_pick.json manifest ready for `ass-ade assimilate`.

    \\b
    Examples:
        ass-ade cherry-pick scout.json
        ass-ade cherry-pick scout.json --pick 1,3,5
        ass-ade cherry-pick scout.json --pick all --no-interactive
        ass-ade cherry-pick scout.json --action assimilate --no-interactive
        ass-ade cherry-pick scout.json --preview --min-confidence 0.6 --json
        ass-ade cherry-pick /path/to/sibling-repo --target .
    """
    from ass_ade.a3_og_features.cherry_feature import preview_cherry_pick, run_cherry_pick

    action_set: set[str] | None = None
    if action and action != "all":
        action_set = {action}

    if preview:
        try:
            result = preview_cherry_pick(
                source=source,
                target_root=target.resolve(),
                actions=action_set,
                min_confidence=min_confidence,
            )
        except (ValueError, OSError) as exc:
            console.print(f"[red]cherry-pick preview error:[/red] {exc}")
            raise typer.Exit(1) from exc

        if print_json:
            typer.echo(json.dumps(result, indent=2))
        elif not quiet:
            total = result["summary"]["total"]
            console.print(f"[bold]Preview:[/bold] {total} candidate(s)")
            for a, count in result["summary"]["actions"].items():
                console.print(f"  {a}: {count}")
        return

    effective_interactive = interactive and pick is None

    try:
        manifest = run_cherry_pick(
            source=source,
            target_root=target.resolve(),
            pick=pick,
            actions=action_set,
            interactive=effective_interactive,
            out_path=out,
            console_print=not quiet,
            min_confidence=min_confidence,
        )
    except (ValueError, OSError) as exc:
        console.print(f"[red]cherry-pick error:[/red] {exc}")
        raise typer.Exit(1) from exc

    if print_json:
        typer.echo(json.dumps(manifest, indent=2))
