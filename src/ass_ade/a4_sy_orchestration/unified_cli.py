"""United ASS-ADE CLI — one command for the CNA book and Atomadic engine.

This module is the **operator-facing** single entry while the source still has
two package roots in one checkout. It exposes:

- top-level Atomadic engine commands such as ``rebuild``, ``enhance``, ``docs``,
  ``lint``, ``certify``, ``nexus``, ``agent``, and ``a2a``.
- ``book`` — full monadic pipeline (phases 0–7, certify, synth-tests).
- ``assimilate`` — multi-root ingest into the monadic book.
- ``ade`` — workspace operator materialization and checks.

The public console scripts are ``ass-ade`` and ``atomadic`` aliases to this app.
"""

from __future__ import annotations

import importlib
import json
import sys
from pathlib import Path
from typing import Annotated, Any

import typer

from ass_ade.a1_at_functions.assimilate_plan_emit import build_validate_assimilate_plan
from ass_ade.a1_at_functions.assimilate_policy_gate import (
    assimilation_policy_gate_enforced,
    load_and_validate_assimilate_policy,
)
from ass_ade.a4_sy_orchestration.cli import app as book_app

# Inventory scanner import
from ass_ade.a1_at_functions.inventory_scan import scan_umbrella

app = typer.Typer(
    no_args_is_help=True,
    help=(
        "ASS-ADE: one Atomadic Development Environment CLI with the restored "
        "engine surface, monadic book pipeline, multi-root assimilate, and ADE "
        "operator tooling."
    ),
)


# --- Inventory command ---
@app.command("inventory")
def inventory(
    roots: Annotated[list[str], typer.Option(
        "--root", "-r", help="Directories to scan (can be repeated)", show_default=True
    )] = ["."],
    format: Annotated[str, typer.Option("--format", "-f", help="Output format: json or table")] = "json",
):
    """Discover sibling repos and terrain."""
    result = scan_umbrella(roots)
    if format == "json":
        typer.echo(json.dumps(result, indent=2))
    else:
        # Simple table output (fallback if tabulate not installed)
        candidates = result["candidates"]
        if not candidates:
            typer.echo("No candidates found.")
            return
        headers = list(candidates[0].keys())
        row_lines = [" | ".join(headers)]
        row_lines.append("-|-" * len(headers))
        for cand in candidates:
            row_lines.append(" | ".join(str(cand[h]) if cand[h] is not None else "" for h in headers))
        typer.echo("\n".join(row_lines))


def _checkout_root() -> Path:
    return Path(__file__).resolve().parents[4]


def _bundled_engine_src() -> Path:
    return _checkout_root() / "atomadic-engine" / "src"


def _bundled_engine_pkg() -> Path:
    return _bundled_engine_src() / "ass_ade"


def _is_under(path: Path, root: Path) -> bool:
    try:
        path.resolve().relative_to(root.resolve())
    except ValueError:
        return False
    return True


def _module_resolves_under(module: Any, root: Path) -> bool:
    module_file = getattr(module, "__file__", None)
    if module_file:
        return _is_under(Path(module_file), root)
    module_paths = getattr(module, "__path__", ())
    return any(_is_under(Path(path), root) for path in module_paths)


def _ensure_bundled_engine_first() -> None:
    """Prefer this checkout's restored ``ass_ade`` over older editable installs."""
    engine_src = _bundled_engine_src()
    engine_pkg = _bundled_engine_pkg()
    if not engine_pkg.exists():
        return

    resolved_engine_src = engine_src.resolve()
    sys.path[:] = [
        path
        for path in sys.path
        if not path or Path(path).resolve() != resolved_engine_src
    ]
    sys.path.insert(0, str(engine_src))

    imported = sys.modules.get("ass_ade")
    if imported is not None and not _module_resolves_under(imported, engine_pkg):
        for name in list(sys.modules):
            if name == "ass_ade" or name.startswith("ass_ade."):
                del sys.modules[name]


def _typer_command_name(command_info: Any) -> str | None:
    name = getattr(command_info, "name", None)
    if name:
        return str(name)
    callback = getattr(command_info, "callback", None)
    if callback is None:
        return None
    from typer.main import get_command_name

    return get_command_name(callback.__name__)


def _registered_cli_names(target: typer.Typer) -> set[str]:
    names: set[str] = set()
    for command_info in target.registered_commands:
        name = _typer_command_name(command_info)
        if name:
            names.add(name)
    for group_info in target.registered_groups:
        name = getattr(group_info, "name", None)
        if name:
            names.add(str(name))
    return names


def _merge_atomadic_surface(source: typer.Typer) -> None:
    """Flatten non-conflicting Atomadic commands onto the ASS-ADE root app."""
    existing = _registered_cli_names(app)
    for command_info in source.registered_commands:
        name = _typer_command_name(command_info)
        if name and name in existing:
            continue
        app.registered_commands.append(command_info)
        if name:
            existing.add(name)
    for group_info in source.registered_groups:
        name = getattr(group_info, "name", None)
        if name and str(name) in existing:
            continue
        app.registered_groups.append(group_info)
        if name:
            existing.add(str(name))


@app.command("assimilate")
def assimilate_cmd(
    primary: Annotated[
        Path,
        typer.Argument(
            exists=True,
            file_okay=False,
            dir_okay=True,
            resolve_path=True,
            help="Primary MAP terrain (wins on duplicate symbols).",
        ),
    ],
    output: Annotated[
        Path,
        typer.Argument(
            file_okay=False,
            dir_okay=True,
            resolve_path=True,
            help="Output parent: materialized monadic tree is created under this directory.",
        ),
    ],
    also: Annotated[
        list[Path],
        typer.Option(
            "--also",
            exists=True,
            file_okay=False,
            dir_okay=True,
            resolve_path=True,
            help="Additional sibling/orphan repo roots merged after PRIMARY.",
        ),
    ] = [],
    policy: Annotated[
        Path | None,
        typer.Option(
            "--policy",
            exists=True,
            file_okay=True,
            dir_okay=False,
            resolve_path=True,
            help=(
                "YAML assimilate policy (see .ass-ade/specs/assimilate-policy.schema.json). "
                "Required when using --also under CI (CI=true) or ASS_ADE_ASSIMILATE_REQUIRE_POLICY=1."
            ),
        ),
    ] = None,
    stop_after: Annotated[
        str,
        typer.Option(
            "--stop-after",
            case_sensitive=False,
            help="Halt after this phase (same labels as `book rebuild`).",
        ),
    ] = "package",
    rebuild_tag: Annotated[
        str | None,
        typer.Option("--rebuild-tag", help="Directory name under output (default: UTC tag)."),
    ] = None,
    distribution_name: Annotated[
        str,
        typer.Option(
            "--distribution-name",
            help="Emitted pyproject [project] name when stop-after reaches package.",
        ),
    ] = "ass-ade-assimilated",
    output_package_name: Annotated[
        str | None,
        typer.Option(
            "--output-package-name",
            help=(
                "Optional Python package root for emitted trees. "
                "Example: `ass_ade` writes under `src/ass_ade/...` and rewrites "
                "materialized imports to that package prefix."
            ),
        ),
    ] = None,
    json_out: Annotated[
        Path | None,
        typer.Option(
            "--json-out",
            file_okay=True,
            dir_okay=False,
            help="Write the full book result as JSON.",
        ),
    ] = None,
    plan_out: Annotated[
        Path | None,
        typer.Option(
            "--plan-out",
            file_okay=True,
            dir_okay=False,
            help="Write ASSIMILATE_PLAN.json (B1/B2) validated against .ass-ade/specs/assimilate-plan.schema.json.",
        ),
    ] = None,
    task_description: Annotated[
        str,
        typer.Option("--task-description", help="Phase 0 recon label."),
    ] = "assimilate",
) -> None:
    """Ingest PRIMARY plus optional --also siblings; rebuild through the monadic book (CNA tiers).

    One-shot path toward Atomadic structure: recon → ingest → gapfill → … →
    package (default). Requires ``--output`` whenever ``--stop-after`` is
    ``materialize`` or later (same as ``book rebuild``).
    """
    from ass_ade.a3_og_features.pipeline_book import run_book_until, stop_after_from_label

    try:
        stop_n = stop_after_from_label(stop_after)
    except ValueError as exc:
        typer.secho(str(exc), fg="red", err=True)
        raise typer.Exit(2) from exc

    if stop_n >= 5 and output is None:
        typer.secho(
            "OUTPUT is required when --stop-after is materialize, audit, or package.",
            fg="red",
            err=True,
        )
        raise typer.Exit(2)

    if also and assimilation_policy_gate_enforced():
        if policy is None:
            typer.secho(
                "Multi-root assimilate (--also) requires --policy when CI=true or "
                "ASS_ADE_ASSIMILATE_REQUIRE_POLICY is set (ASS_ADE_SHIP_PLAN S2).",
                fg="red",
                err=True,
            )
            raise typer.Exit(2)
    policy_doc: dict[str, Any] | None = None
    if policy is not None:
        try:
            policy_doc = load_and_validate_assimilate_policy(policy)
        except (OSError, UnicodeError, ValueError, RuntimeError) as exc:
            typer.secho(f"Invalid assimilate policy: {exc}", fg="red", err=True)
            raise typer.Exit(2) from exc

    book: dict[str, Any] = run_book_until(
        primary,
        output,
        stop_after=stop_n,
        rebuild_tag=rebuild_tag,
        task_description=task_description,
        extra_source_roots=also or None,
        distribution_name=distribution_name,
        output_package_name=output_package_name,
        policy_doc=policy_doc,
    )
    if policy_doc is not None:
        book = {**book, "assimilate_policy": policy_doc}

    try:
        plan_doc = build_validate_assimilate_plan(
            book=book,
            primary=primary,
            output_parent=output,
            extra_roots=list(also),
            stop_after_label=stop_after,
            policy=policy_doc,
        )
    except (ValueError, RuntimeError) as exc:
        typer.secho(f"ASSIMILATE_PLAN validation failed: {exc}", fg="red", err=True)
        raise typer.Exit(2) from exc
    book = {**book, "ASSIMILATE_PLAN": plan_doc}

    if plan_out is not None:
        plan_out.parent.mkdir(parents=True, exist_ok=True)
        plan_out.write_text(json.dumps(plan_doc, indent=2, default=str) + "\n", encoding="utf-8")

    if json_out is not None:
        json_out.parent.mkdir(parents=True, exist_ok=True)
        json_out.write_text(json.dumps(book, indent=2, default=str) + "\n", encoding="utf-8")

    summary: dict[str, Any] = {
        "command": "assimilate",
        "stopped_after": book.get("stopped_after"),
        "rebuild_tag": book.get("rebuild_tag"),
        "verdict": (book.get("phase0") or {}).get("verdict"),
        "extra_roots": [str(p) for p in also],
    }
    if policy_doc is not None:
        summary["policy_schema_version"] = policy_doc.get("schema_version")
    summary["assimilate_plan_schema_version"] = plan_doc.get("schema_version")
    typer.echo(json.dumps(summary, indent=2))

    p0 = book.get("phase0") or {}
    if p0.get("verdict") != "READY_FOR_PHASE_1" and stop_n > 0:
        raise typer.Exit(1)
    if stop_n >= 6:
        audit = (book.get("phase6") or {}).get("audit") or {}
        audit_summary = audit.get("summary") or {}
        if not audit_summary.get("structure_conformant"):
            raise typer.Exit(1)


@app.command("doctor")
def doctor_cmd(
    no_remote: Annotated[
        bool,
        typer.Option("--no-remote", help="Skip remote connectivity checks (for offline/CI use)."),
    ] = False,
) -> None:
    """Show which ASS-ADE surfaces are available in this environment."""
    _ensure_bundled_engine_first()
    checkout_root = _checkout_root()
    expected_v11 = checkout_root / "ass-ade-v1.1" / "src" / "ass_ade"
    expected_engine = _bundled_engine_pkg()
    v11_file = Path(__file__).resolve()
    lines = [
        f"[ass-ade] checkout root: {checkout_root}",
        f"[ass-ade] monadic pipeline: OK -> {v11_file}",
        "[ass-ade] one-shot sibling ingest: `ass-ade assimilate PRIMARY OUTPUT [--also PATH ...]`",
        "[ass-ade] multi-root policy: under CI (or ASS_ADE_ASSIMILATE_REQUIRE_POLICY=1), `--also` requires `--policy` YAML",
        "[ass-ade] assimilate emits `ASSIMILATE_PLAN` (see `--plan-out` + book JSON `ASSIMILATE_PLAN` key)",
    ]
    if expected_v11.exists() and not _is_under(v11_file, expected_v11):
        lines.append(f"[ass-ade] WARNING: monadic package is not resolving under {expected_v11}")
    try:
        ass_ade = importlib.import_module("ass_ade")
        ass_ade_file = Path(getattr(ass_ade, "__file__", "") or "")
        ass_ade_location = str(ass_ade_file.resolve()) if ass_ade_file else "namespace package"
        lines.append(f"[ass-ade] engine package (ass_ade): OK -> {ass_ade_location}")
        if expected_engine.exists() and ass_ade_file and not _is_under(ass_ade_file, expected_engine):
            lines.append(f"[ass-ade] WARNING: ass_ade is not resolving under {expected_engine}")
        try:
            cli_mod = importlib.import_module("ass_ade.cli")
            cli_file = Path(getattr(cli_mod, "__file__", "") or "")
            cli_location = str(cli_file.resolve()) if cli_file else "namespace package"
            lines.append(f"[ass-ade] engine CLI: OK -> {cli_location}")
            lines.append("[ass-ade] CLI aliases: `ass-ade ...` and `atomadic ...`")
        except ImportError as exc:
            lines.append(f"[ass-ade] engine CLI: MISSING -> {exc}")
    except ImportError:
        lines.append(
            "[ass-ade] ass_ade engine package: MISSING -> install this repo root with "
            "`pip install -e \".[dev]\"` so `import ass_ade` resolves"
        )
    typer.echo("\n".join(lines))


app.add_typer(book_app, name="book")

from ass_ade.ade.cli import app as ade_app  # noqa: E402  — after `app` exists
from ass_ade.a4_sy_orchestration.discord_cmd import discord_app  # noqa: E402
from ass_ade.a4_sy_orchestration.hello_cmd import hello_app  # noqa: E402

# ── discord sub-app ────────────────────────────────────────────────────────────

_discord_app = typer.Typer(help="Atomadic Discord bot commands.")


@_discord_app.command("start")
def discord_start(
    token: Annotated[
        str,
        typer.Option("--token", envvar="DISCORD_BOT_TOKEN", help="Discord bot token."),
    ] = "",
) -> None:
    """Start the Atomadic Discord bot (blocks until Ctrl-C)."""
    import sys

    sys.path.insert(0, str(Path(__file__).resolve().parents[4] / "scripts"))
    try:
        from atomadic_discord_bot import run  # type: ignore[import]
    except ImportError as exc:
        typer.secho(
            f"discord bot unavailable — install discord.py: pip install discord.py ({exc})",
            fg="red",
            err=True,
        )
        raise typer.Exit(1) from exc
    run(token or None)


app.add_typer(_discord_app, name="discord")

# ── hello sub-app ──────────────────────────────────────────────────────────────

_hello_app = typer.Typer(help="hello.atomadic.tech Cloudflare Worker commands.")


@_hello_app.command("deploy")
def hello_deploy(
    env: Annotated[
        str,
        typer.Option("--env", help="Wrangler environment (e.g. production)."),
    ] = "",
) -> None:
    """Deploy hello_worker.js to Cloudflare via wrangler."""
    import subprocess

    scripts_dir = Path(__file__).resolve().parents[4] / "scripts"
    wrangler_toml = scripts_dir / "wrangler.toml"
    if not wrangler_toml.exists():
        typer.secho(f"wrangler.toml not found at {wrangler_toml}", fg="red", err=True)
        raise typer.Exit(1)
    cmd = ["wrangler", "deploy"]
    if env:
        cmd += ["--env", env]
    typer.echo(f"[hello] running: {' '.join(cmd)} (cwd={scripts_dir})")
    result = subprocess.run(cmd, cwd=str(scripts_dir))
    raise typer.Exit(result.returncode)


app.add_typer(_hello_app, name="hello")

# ── heartbeat sub-app ──────────────────────────────────────────────────────────

_heartbeat_app = typer.Typer(help="Atomadic heartbeat daemon (Cloudflare Worker).")


@_heartbeat_app.command("deploy")
def heartbeat_deploy(
    env: Annotated[
        str,
        typer.Option("--env", help="Wrangler environment (e.g. production)."),
    ] = "",
) -> None:
    """Deploy heartbeat_worker.js to Cloudflare via wrangler."""
    import subprocess

    scripts_dir = Path(__file__).resolve().parents[4] / "scripts"
    config = scripts_dir / "wrangler.heartbeat.toml"
    if not config.exists():
        typer.secho(f"wrangler.heartbeat.toml not found at {config}", fg="red", err=True)
        raise typer.Exit(1)
    cmd = ["wrangler", "deploy", "--config", str(config)]
    if env:
        cmd += ["--env", env]
    typer.echo(f"[heartbeat] running: {' '.join(cmd)} (cwd={scripts_dir})")
    result = subprocess.run(cmd, cwd=str(scripts_dir))
    raise typer.Exit(result.returncode)


app.add_typer(_heartbeat_app, name="heartbeat")

app.add_typer(ade_app, name="ade")
app.add_typer(discord_app, name="discord")
app.add_typer(hello_app, name="hello")

_ensure_bundled_engine_first()

try:  # pragma: no cover - optional legacy Typer studio (v1 tree)
    from ass_ade.cli import app as studio_app
except ImportError:
    studio_app = None

if studio_app is not None:
    _merge_atomadic_surface(studio_app)


@app.command(
    "atomadic",
    context_settings={
        "allow_extra_args": True,
        "ignore_unknown_options": True,
        # Do not register Typer's own ``--help`` on this shim; forward argv to Click
        # so ``… atomadic build --help`` reaches the ``build`` subcommand.
        "help_option_names": [],
    },
    hidden=True,
    help=(
        "Atomadic rebuild engine: rebuild, enhance, docs, lint, certify, forge, Nexus, MCP, A2A. "
        "Legacy ``build`` is accepted as an alias for ``rebuild``. Use ``… atomadic --help`` for top-level; "
        "``… atomadic build --help`` for a subcommand."
    ),
)
def atomadic_proxy(ctx: typer.Context) -> None:
    """Delegate to the bundled :mod:`ass_ade.cli` Typer app."""
    _run_atomadic_command(list(ctx.args), prog_name="ass-ade atomadic")


@app.command(
    "build",
    context_settings={
        "allow_extra_args": True,
        "ignore_unknown_options": True,
        "help_option_names": [],
    },
    hidden=True,
)
def build_proxy(ctx: typer.Context) -> None:
    """Legacy alias for ``rebuild``."""
    _run_atomadic_command(["build", *ctx.args], prog_name="ass-ade")


def _run_atomadic_command(argv: list[str], *, prog_name: str) -> None:
    """Delegate argv to the bundled :mod:`ass_ade.cli` Typer app."""
    _ensure_bundled_engine_first()
    try:
        from typer.main import get_command

        from ass_ade.cli import app as _atomadic_app
    except ImportError as exc:  # pragma: no cover
        typer.secho(f"atomadic engine unavailable: {exc}", fg="red", err=True)
        raise typer.Exit(2) from exc
    argv = list(argv)
    if argv and argv[0] == "build":
        argv[0] = "rebuild"
    command = get_command(_atomadic_app)
    try:
        command.main(args=argv, prog_name=prog_name)
    except SystemExit as exc:
        raise typer.Exit(exc.code) from exc


def atomadic_main() -> None:
    """Backward-compatible console script entry for old editable installs."""
    main()


def main() -> None:
    """Console script entry (``ass-ade`` / ``atomadic``)."""
    app()


if __name__ == "__main__":
    main()
