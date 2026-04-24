"""Typer CLI - ASS-ADE rebuild book (phases 0-7, --stop-after)."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Annotated, Any

import typer

from ass_ade.a1_at_functions.audit_rebuild import validate_rebuild_v11
from ass_ade.a3_og_features.pipeline_book import (
    STOP_AFTER_LABELS,
    run_book_until,
    stop_after_from_label,
)

app = typer.Typer(
    no_args_is_help=True,
    help=(
        "ASS-ADE monadic rebuild: recon -> ingest -> gap-fill -> enrich -> "
        "validate -> materialize -> audit -> package. "
        "Use --stop-after to halt after a named phase. "
        "``certify`` fingerprints a materialized tier tree. "
        "``synth-tests`` regenerates import-smoke manifest under tests/generated_smoke/."
    ),
)


def _version_callback(value: bool) -> None:
    if value:
        try:
            from importlib.metadata import version as pkg_version
        except ImportError:
            typer.echo("ass-ade (version metadata unavailable)", err=True)
            raise typer.Exit(0)
        typer.echo(pkg_version("ass-ade"))
        raise typer.Exit(0)


@app.callback()
def _root(
    _version: Annotated[
        bool,
        typer.Option("--version", callback=_version_callback, is_eager=True),
    ] = False,
) -> None:
    """Global options (e.g. ``--version``)."""


@app.command("rebuild")
def rebuild_cmd(
    source: Annotated[
        Path,
        typer.Argument(
            exists=True,
            file_okay=False,
            dir_okay=True,
            resolve_path=True,
            help="Source tree root (default: current directory).",
        ),
    ] = Path("."),
    output: Annotated[
        Path | None,
        typer.Option(
            "--output",
            "-o",
            file_okay=False,
            dir_okay=True,
            resolve_path=True,
            help="Output parent for phases materialize+ (required when --stop-after is materialize or later).",
        ),
    ] = None,
    stop_after: Annotated[
        str,
        typer.Option(
            "--stop-after",
            help=f"Halt after this phase: {', '.join(STOP_AFTER_LABELS)}.",
            case_sensitive=False,
        ),
    ] = "package",
    rebuild_tag: Annotated[
        str | None,
        typer.Option("--rebuild-tag", help="Directory name under output (default: UTC timestamp)."),
    ] = None,
    task_description: Annotated[
        str,
        typer.Option("--task-description", help="Phase 0 recon task label."),
    ] = "rebuild",
    distribution_name: Annotated[
        str,
        typer.Option("--distribution-name", help="Emitted pyproject [project] name (phase 7)."),
    ] = "ass-ade-rebuilt",
    output_package_name: Annotated[
        str | None,
        typer.Option(
            "--output-package-name",
            help=(
                "Optional Python package root for emitted trees. "
                "Example: `ass_ade` writes tiers under `src/ass_ade/...` "
                "and rewrites materialized imports to that package prefix."
            ),
        ),
    ] = None,
    json_out: Annotated[
        Path | None,
        typer.Option(
            "--json-out",
            file_okay=True,
            dir_okay=False,
            help="Write the result book as JSON to this path.",
        ),
    ] = None,
    no_break_cycles: Annotated[
        bool,
        typer.Option("--no-break-cycles", help="Do not break cycles in phase 4 (report only)."),
    ] = False,
    no_enforce_purity: Annotated[
        bool,
        typer.Option("--no-enforce-purity", help="Skip tier-purity edge removal in phase 4."),
    ] = False,
    also: Annotated[
        list[Path],
        typer.Option(
            "--also",
            exists=True,
            file_okay=False,
            dir_okay=True,
            resolve_path=True,
            help="Additional source root(s) merged after SOURCE; primary wins on duplicate symbols.",
        ),
    ] = [],
) -> None:
    """Run the rebuild book up to the phase set by --stop-after."""
    try:
        stop_n = stop_after_from_label(stop_after)
    except ValueError as exc:
        typer.secho(str(exc), fg="red", err=True)
        raise typer.Exit(2) from exc

    if stop_n >= 5 and output is None:
        typer.secho(
            "--output / -o is required for --stop-after materialize, audit, or package.",
            fg="red",
            err=True,
        )
        raise typer.Exit(2)

    book: dict[str, Any] = run_book_until(
        source,
        output,
        stop_after=stop_n,
        rebuild_tag=rebuild_tag,
        task_description=task_description,
        extra_source_roots=also or None,
        break_cycles_if_found=not no_break_cycles,
        enforce_purity=not no_enforce_purity,
        distribution_name=distribution_name,
        output_package_name=output_package_name,
    )

    if json_out is not None:
        json_out.parent.mkdir(parents=True, exist_ok=True)
        json_out.write_text(json.dumps(book, indent=2, default=str) + "\n", encoding="utf-8")

    typer.echo(
        json.dumps(
            {
                "stopped_after": book.get("stopped_after"),
                "rebuild_tag": book.get("rebuild_tag"),
                "verdict": (book.get("phase0") or {}).get("verdict"),
            },
            indent=2,
        )
    )

    p0 = book.get("phase0") or {}
    if p0.get("verdict") != "READY_FOR_PHASE_1" and stop_n > 0:
        raise typer.Exit(1)
    if stop_n >= 6:
        audit = (book.get("phase6") or {}).get("audit") or {}
        summary = audit.get("summary") or {}
        if not summary.get("structure_conformant"):
            raise typer.Exit(1)


@app.command("certify")
def certify_cmd(
    target: Annotated[
        Path,
        typer.Argument(
            exists=True,
            file_okay=False,
            dir_okay=True,
            resolve_path=True,
            help="Materialized rebuild root (tier directories with JSON sidecars).",
        ),
    ],
    json_out: Annotated[
        Path | None,
        typer.Option(
            "--json-out",
            file_okay=True,
            dir_okay=False,
            help="Write full audit payload as JSON.",
        ),
    ] = None,
) -> None:
    """Validate a materialized tree (phase-6 audit only; MAP=TERRAIN)."""
    audit = validate_rebuild_v11(target)
    if json_out is not None:
        json_out.parent.mkdir(parents=True, exist_ok=True)
        json_out.write_text(json.dumps(audit, indent=2, default=str) + "\n", encoding="utf-8")

    summary = audit.get("summary") or {}
    typer.echo(
        json.dumps(
            {
                "target_root": audit.get("target_root"),
                "structure_conformant": summary.get("structure_conformant"),
                "total": audit.get("total"),
                "valid": audit.get("valid"),
                "pass_rate": summary.get("pass_rate"),
            },
            indent=2,
        )
    )
    if not summary.get("structure_conformant"):
        raise typer.Exit(1)


@app.command("synth-tests")
def synth_tests_cmd(
    check: Annotated[
        bool,
        typer.Option(
            "--check",
            help="Verify tests/generated_smoke/_qualnames.json matches src (CI gate).",
        ),
    ] = False,
    repo: Annotated[
        Path,
        typer.Option(
            "--repo",
            exists=True,
            file_okay=False,
            dir_okay=True,
            resolve_path=True,
            help="Repository root (contains src/ and tests/).",
        ),
    ] = Path("."),
) -> None:
    """Regenerate import-manifest for parametrized smoke tests (MAP=TERRAIN)."""
    from ass_ade.a1_at_functions.test_synth_plan import manifest_drift
    from ass_ade.a3_og_features.emit_test_manifest import run_emit_test_manifest

    rr = repo.resolve()
    if check:
        drift = manifest_drift(rr)
        if not drift["ok"]:
            typer.secho(json.dumps(drift, indent=2, default=str), fg="red", err=True)
            raise typer.Exit(1)
        typer.echo("synth-tests: manifest matches sources")
        return
    out = run_emit_test_manifest(rr)
    typer.echo(json.dumps(out, indent=2))


def main() -> None:
    """Book CLI runner used by the merged ``ass-ade book`` command."""
    app()


if __name__ == "__main__":
    main()
