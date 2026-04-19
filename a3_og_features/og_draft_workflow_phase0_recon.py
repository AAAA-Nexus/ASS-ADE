# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a3_og_features/og_draft_workflow_phase0_recon.py:7
# Component id: og.source.a3_og_features.workflow_phase0_recon
from __future__ import annotations

__version__ = "0.1.0"

def workflow_phase0_recon(
    task_description: str = typer.Argument(..., help="Task to recon before execution."),
    source: list[str] = typer.Option([], "--source", help="Official source URL already researched."),
    path: Path = REPO_PATH_OPTION,
    max_files: int = typer.Option(20, help="Maximum relevant files to return."),
    json_out: bool = typer.Option(False, "--json", help="Output raw JSON."),
) -> None:
    """Never Code Blind gate: repo recon plus required latest-doc source targets."""
    from ass_ade.recon import phase0_recon

    result = phase0_recon(
        task_description=task_description,
        working_dir=path,
        provided_sources=source,
        max_relevant_files=max_files,
    )

    if json_out:
        _print_json(result.model_dump(), redact=True)
        return

    color = "green" if result.verdict == "READY_FOR_PHASE_1" else "yellow"
    console.print(f"[{color}]Phase 0 Recon: {result.verdict}[/{color}]")
    if result.research_targets:
        console.print("[bold]Research targets:[/bold]")
        for target in result.research_targets:
            hint = f" ({target.suggested_url})" if target.suggested_url else ""
            console.print(f"  - {target.topic}{hint}")
    if result.codebase.relevant_files:
        console.print("[bold]Relevant files:[/bold]")
        for rel in result.codebase.relevant_files:
            console.print(f"  - {rel}")
    if result.required_actions:
        console.print("[bold]Required before code:[/bold]")
        for action in result.required_actions:
            console.print(f"  - {action}")
    console.print(f"Next: {result.next_action}")
