# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a1_at_functions/at_draft_a2a_negotiate.py:7
# Component id: at.source.a1_at_functions.a2a_negotiate
from __future__ import annotations

__version__ = "0.1.0"

def a2a_negotiate(
    remote_url: Annotated[str, typer.Argument(help="Base URL of the remote agent to negotiate with.")],
    config: Path | None = CONFIG_OPTION,
) -> None:
    """Compare local ASS-ADE agent card with a remote agent for A2A interoperability."""
    from ass_ade.nexus.validation import validate_url

    _, settings = _resolve_config(config)

    try:
        validate_url(remote_url)
    except ValueError as exc:
        console.print(f"[red]Blocked:[/red] {exc}")
        raise typer.Exit(code=1) from exc

    local = local_agent_card(str(Path(".").resolve()))
    report = fetch_agent_card(remote_url)
    if not report.valid or not report.card:
        msgs = [issue.message for issue in report.errors]
        console.print(f"[red]Remote agent card invalid:[/red] {msgs}")
        raise typer.Exit(code=1)

    result = negotiate(local, report.card)
    console.print(json.dumps({
        "compatible": result.compatible,
        "shared_skills": result.shared_skills,
        "local_only": result.local_only,
        "remote_only": result.remote_only,
        "auth_compatible": result.auth_compatible,
        "notes": result.notes,
    }, indent=2), markup=False)
    if not result.compatible:
        raise typer.Exit(code=1)
