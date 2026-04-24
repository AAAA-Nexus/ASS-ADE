"""``ass-ade ade ...`` - materialize and verify the workspace operator tree."""

from __future__ import annotations

from pathlib import Path
from typing import Annotated, Optional

import json

import typer

from ass_ade_v11.ade.materialize import materialize_dotted_ade
from ass_ade_v11.ade.staging_handoff import (
    DEFAULT_REQUIRED_SHIP_PATHS,
    build_staging_handoff_summary,
)

app = typer.Typer(
    no_args_is_help=True,
    help="ADE workspace: ship the Atomadic/ADE operator stack (hooks, automation) into .ade/",
)


@app.command("materialize")
def materialize_cmd(
    workspace: Annotated[
        Path,
        typer.Argument(
            file_okay=False,
            dir_okay=True,
            resolve_path=True,
            help="Project root (default: current directory).",
        ),
    ] = Path("."),
    source: Annotated[
        Optional[Path],
        typer.Option(
            "--source",
            exists=True,
            file_okay=False,
            help="Path to the Atomadic / ass-ade monorepo (where agents/INDEX.md lives).",
        ),
    ] = None,
    with_agents: Annotated[
        bool,
        typer.Option(
            "--with-agents",
            help="Copy all agent *.prompt.md files into .ade/agents-core/ (large).",
        ),
    ] = False,
    no_cursor: Annotated[
        bool,
        typer.Option(
            "--no-cursor",
            help="Do not copy into <workspace>/.cursor/hooks (only populate .ade/).",
        ),
    ] = False,
    no_vscode: Annotated[
        bool,
        typer.Option(
            "--no-vscode",
            help="Do not merge .vscode/extensions.json (Copilot + Python) recommendations.",
        ),
    ] = False,
) -> None:
    """Create ``.ade/`` and (by default) install ``.cursor/hooks`` in the target workspace."""
    ws = workspace.resolve()
    r = materialize_dotted_ade(
        ws,
        source=source,
        with_agents=with_agents,
        install_cursor=not no_cursor,
        merge_vscode_recommendations=not no_vscode,
    )
    typer.echo(
        f"OK — ADE materialized: {r.ade_dir}\n  source: {r.source_root}\n"
        f"  files copied: {r.files_written}\n  cursor hooks installed: {r.cursor_installed}"
    )


@app.command("install-cursor")
def install_cursor_cmd(
    workspace: Annotated[
        Optional[Path],
        typer.Argument(
            file_okay=False,
            dir_okay=True,
            help="Project root; default: cwd. Requires existing .ade/cursor-hooks from materialize.",
        ),
    ] = None,
) -> None:
    """Copy ``.ade/cursor-hooks/`` to ``.cursor/hooks/``; copy root ``.cursor/hooks.json`` if present in source (see env)."""
    import shutil

    from ass_ade_v11.ade.discover import find_monorepo_root

    ws = (workspace or Path.cwd()).resolve()
    ade = ws / ".ade" / "cursor-hooks"
    if not ade.is_dir():
        raise typer.BadParameter(
            f"Expected {ade} (run `ass-ade ade materialize` in this project first.)"
        )
    dst = ws / ".cursor" / "hooks"
    dst.mkdir(parents=True, exist_ok=True)
    n = 0
    for f in ade.iterdir():
        if f.is_file():
            shutil.copy2(f, dst / f.name)
            n += 1
    root = find_monorepo_root(None)
    if root is not None:
        h = root / ".cursor" / "hooks.json"
        if h.is_file():
            ws.mkdir(parents=True, exist_ok=True)
            (ws / ".cursor").mkdir(parents=True, exist_ok=True)
            shutil.copy2(h, ws / ".cursor" / "hooks.json")
            n += 1
    typer.echo(f"OK — {n} file(s) into {dst} (+ hooks.json if available from monorepo discovery)")


@app.command("doctor")
def doctor_ade() -> None:
    """Show whether a workspace has ``.ade/`` and whether the monorepo is discoverable."""
    from ass_ade_v11.ade.discover import ass_ade_v11_package_dir, find_monorepo_root

    root = find_monorepo_root(None)
    ws = Path.cwd()
    typer.echo(f"[ade] ass_ade_v11.ade package: {ass_ade_v11_package_dir()}")
    if root is not None:
        typer.echo(f"[ade] monorepo discovered: {root} (OK)")
    else:
        typer.echo(
            "[ade] monorepo: NOT found — set ATOMADIC_WORKSPACE to your Atomadic/ass-ade clone "
            "or pass `ade materialize --source PATH`."
        )
    ade = ws / ".ade"
    if (ade / "LAYOUT.json").is_file():
        typer.echo(f"[ade] workspace {ws} has .ade/ (LAYOUT present) — good.")
    else:
        typer.echo(
            f"[ade] no .ade/ in {ws} - run `ass-ade ade materialize` after checkout."
        )


@app.command("ship-audit")
def ship_audit_cmd(
    staging_root: Annotated[
        Optional[Path],
        typer.Option(
            "--staging-root",
            file_okay=False,
            dir_okay=True,
            resolve_path=True,
            help=(
                "Public staging checkout or its parent !aaaa-nexus directory. "
                "Defaults to ATOMADIC_NEXUS_SHIP_ROOT / ATOMADIC_NEXUS_WORKSPACE / sibling C:\\!aaaa-nexus\\!ass-ade."
            ),
        ),
    ] = None,
    private_root: Annotated[
        Optional[Path],
        typer.Option(
            "--private-root",
            exists=True,
            file_okay=False,
            dir_okay=True,
            resolve_path=True,
            help="Private monorepo root; default uses ADE monorepo discovery.",
        ),
    ] = None,
    use_default_paths: Annotated[
        bool,
        typer.Option(
            "--default-paths/--no-default-paths",
            help="Include the built-in ASS-ADE ship-surface file checks.",
        ),
    ] = True,
    require_path: Annotated[
        list[str],
        typer.Option(
            "--require-path",
            help="Additional relative file path to require in both private and staging trees; repeatable.",
        ),
    ] = [],
    json_out: Annotated[
        Optional[Path],
        typer.Option(
            "--json-out",
            file_okay=True,
            dir_okay=False,
            resolve_path=True,
            help="Optional file path to write the audit JSON.",
        ),
    ] = None,
) -> None:
    """Verify that the scrubbed staging checkout is clean, git-backed, and aligned before push."""
    required_paths = list(DEFAULT_REQUIRED_SHIP_PATHS) if use_default_paths else []
    required_paths.extend(require_path)
    summary = build_staging_handoff_summary(
        private_root=private_root,
        staging_root=staging_root,
        required_paths=required_paths,
    )
    payload = json.dumps(summary, indent=2) + "\n"
    if json_out is not None:
        json_out.parent.mkdir(parents=True, exist_ok=True)
        json_out.write_text(payload, encoding="utf-8")
    typer.echo(payload, nl=False)
    if not summary.get("ok", False):
        raise typer.Exit(1)
