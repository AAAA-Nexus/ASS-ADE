"""United ASS-ADE CLI — CNA/monadic ``book`` + optional v1 ``studio`` surface.

This module is the **operator-facing** single entry while source trees still
live in multiple checkouts. It nests:

- ``book`` — full ``ass-ade-v11`` pipeline (phases 0–7, certify, synth-tests).
- ``studio`` — the large ``ass_ade.cli`` Typer application **when** package
  ``ass-ade`` (v1 tree) is installed in the same environment.

Long-term goal: one ``src/`` tree and one distribution; see ``docs/ASS_ADE_UNIFICATION.md``.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Annotated, Any

import typer

from ass_ade_v11.a1_at_functions.assimilate_plan_emit import build_validate_assimilate_plan
from ass_ade_v11.a1_at_functions.assimilate_policy_gate import (
    assimilation_policy_gate_enforced,
    load_and_validate_assimilate_policy,
)
from ass_ade_v11.a4_sy_orchestration.cli import app as book_app

app = typer.Typer(
    no_args_is_help=True,
    help=(
        "United ASS-ADE: ``assimilate`` (multi-root → monadic emit); monadic "
        "``book``; full IDE/Nexus ``studio`` when ``ass_ade`` (v1) is co-installed."
    ),
)


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
    from ass_ade_v11.a3_og_features.pipeline_book import run_book_until, stop_after_from_label

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
def doctor_cmd() -> None:
    """Show which united surfaces are available in this environment."""
    lines = [
        "[united] monadic pipeline (ass_ade_v11): OK — `ass-ade-unified book …`",
        "[united] one-shot sibling ingest: `ass-ade-unified assimilate PRIMARY OUTPUT [--also PATH ...]`",
        "[united] multi-root policy: under CI (or ASS_ADE_ASSIMILATE_REQUIRE_POLICY=1), `--also` requires `--policy` YAML",
        "[united] assimilate emits `ASSIMILATE_PLAN` (see `--plan-out` + book JSON `ASSIMILATE_PLAN` key)",
    ]
    try:
        import ass_ade  # noqa: F401

        lines.append("[united] v1 studio (ass_ade): OK — `ass-ade-unified studio …`")
    except ImportError:
        lines.append(
            "[united] v1 studio (ass_ade): MISSING — install the v1 tree in this venv "
            "(e.g. `pip install -e ./ass-ade-v1`) so `import ass_ade` resolves"
        )
    typer.echo("\n".join(lines))


app.add_typer(book_app, name="book")

from ass_ade_v11.ade.cli import app as ade_app  # noqa: E402  — after `app` exists

app.add_typer(ade_app, name="ade")

try:  # pragma: no cover - optional sibling package
    from ass_ade.cli import app as studio_app
except ImportError:
    studio_app = None

if studio_app is not None:
    app.add_typer(studio_app, name="studio")


def main() -> None:
    """Console script entry (``ass-ade-unified``)."""
    app()


if __name__ == "__main__":
    main()
