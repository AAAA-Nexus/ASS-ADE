"""Tests for the Typer CLI introspector (a2_mo_composites.cli_introspector)."""

from __future__ import annotations

from pathlib import Path
from typing import Annotated

import typer

from ass_ade.a2_mo_composites.cli_introspector import (
    categorize_commands,
    introspect_typer_app,
)


def _build_app() -> typer.Typer:
    app = typer.Typer()

    @app.command("scout")
    def scout(
        repo: Annotated[Path, typer.Argument(help="Repo to scout.")],
        use_llm: Annotated[bool, typer.Option("--llm/--no-llm", help="LLM synthesis.")] = True,
        model: Annotated[str | None, typer.Option("--model", help="Model override.")] = None,
    ) -> None:
        """Scout a repo."""

    @app.command("trust-gate")
    def trust_gate(
        evidence: Annotated[Path, typer.Argument(help="Evidence file.")],
    ) -> None:
        """Run trust gate."""

    return app


def test_introspects_commands_with_params() -> None:
    app = _build_app()
    cmds = introspect_typer_app(app)
    assert [c["name"] for c in cmds] == ["scout", "trust-gate"]

    scout = next(c for c in cmds if c["name"] == "scout")
    assert scout["summary"].startswith("Scout a repo")
    names = [p["name"] for p in scout["params"]]
    assert names == ["repo", "use_llm", "model"]


def test_argument_vs_option_kinds_detected() -> None:
    app = _build_app()
    scout = next(c for c in introspect_typer_app(app) if c["name"] == "scout")
    by_name = {p["name"]: p for p in scout["params"]}
    assert by_name["repo"]["kind"] == "argument"
    assert by_name["use_llm"]["kind"] == "option"
    assert by_name["use_llm"]["default"] is True
    assert by_name["model"]["nullable"] is True


def test_flags_captured_from_option() -> None:
    app = _build_app()
    scout = next(c for c in introspect_typer_app(app) if c["name"] == "scout")
    use_llm = next(p for p in scout["params"] if p["name"] == "use_llm")
    assert "--llm/--no-llm" in use_llm["flags"]


def test_categorize_commands_groups_by_name() -> None:
    app = _build_app()
    cmds = introspect_typer_app(app)
    groups = categorize_commands(cmds)
    assert "scout" in [c["name"] for c in groups.get("Scout & Assimilate", [])]


def test_real_cli_app_introspects_without_error() -> None:
    """Smoke test: the real ass-ade Typer app should introspect cleanly."""
    from ass_ade.cli import app

    cmds = introspect_typer_app(app)
    assert len(cmds) > 10
    names = {c["name"] for c in cmds}
    assert "scout" in names
    assert "ui" in names
